import json

from botocore.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.core.validators import validate_email
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    User, Product, Category, Order, OrderItem, ShoppingCart, CartItem,
    Payment, Review, Wishlist, WishlistItem
)
from .serializers import (
    UserSerializer, ProductSerializer, CategorySerializer, OrderSerializer,
    OrderItemSerializer, ShoppingCartSerializer, CartItemSerializer,
    PaymentSerializer, ReviewSerializer, WishlistSerializer, WishlistItemSerializer
)
from .dynamodb_service import create_order, get_order, update_order_status
from .tasks import process_payment, send_order_confirmation_email
import logging

logger = logging.getLogger('security')

class CachedProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        cache_key = 'products_list'
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        # Оптимизация: выбираем только необходимые поля
        self.queryset = self.queryset.only('id', 'name', 'price', 'category__name')
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 15)  # 15 минут кэша
        return response

    def retrieve(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        cache_key = f'product_{product_id}'
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 10)  # 10 минут кэша
        return response


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('user').prefetch_related('orderitem_set__product')
    serializer_class = OrderSerializer

    def list(self, request, *args, **kwargs):
        cache_key = 'orders_list'
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 10)
        return response



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.only('id', 'username', 'email')  # Оптимизация выбора данных
    serializer_class = UserSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category')
    serializer_class = ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.select_related('order', 'product')
    serializer_class = OrderItemSerializer


class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.select_related('user').prefetch_related('cartitem_set__product')
    serializer_class = ShoppingCartSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.select_related('cart', 'product')
    serializer_class = CartItemSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related('user', 'product')
    serializer_class = ReviewSerializer


class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.select_related('user').prefetch_related('wishlistitem_set__product')
    serializer_class = WishlistSerializer


class WishlistItemViewSet(viewsets.ModelViewSet):
    queryset = WishlistItem.objects.select_related('wishlist', 'product')
    serializer_class = WishlistItemSerializer


from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_ratelimit.decorators import ratelimit
from .tasks import send_order_confirmation_email
from .dynamodb_service import create_order


@api_view(['POST'])
@ratelimit(key='ip', rate='5/m', block=True)
def create_order_view(request):
    """
    Создаёт заказ, добавляет в базу данных и отправляет подтверждение по email.
    """
    data = request.data
    order_id = data.get('orderId')
    user_id = data.get('userId')
    total_amount = data.get('totalAmount')
    customer_email = data.get('customerEmail')

    if not all([order_id, user_id, total_amount, customer_email]):
        return Response({
            "message": "Все поля (orderId, userId, totalAmount, customerEmail) обязательны."
        }, status=400)


    response = create_order(order_id, user_id, total_amount)


    send_order_confirmation_email(order_id=order_id, customer_email=customer_email)

    process_payment(order_id=order_id)

    return Response({
        "message": f"Заказ #{order_id} создан. Email отправлен на {customer_email}. Платеж обрабатывается.",
        "data": response
    })



@api_view(['GET'])
@ratelimit(key='ip', rate='10/m', block=True)
def get_order_view(request, order_id):
    """
    Получает заказ по ID с использованием кэша.
    """
    use_strong_consistency = request.query_params.get('strong', 'false').lower() == 'true'
    cache_key = f'order_{order_id}'
    cached_data = cache.get(cache_key)

    if cached_data:
        return JsonResponse(cached_data, safe=False)

    order = get_order(order_id, use_strong_consistency)

    if order:
        cache.set(cache_key, order, timeout=60 * 10)
        return JsonResponse(order, safe=False)

    return JsonResponse({"message": "Order not found"}, status=404)


@api_view(['PATCH'])
@ratelimit(key='ip', rate='5/m', block=True)
def update_order_view(request, order_id):
    """
    Обновляет статус заказа и очищает кэш.
    """
    data = request.data
    status = data.get('status')


    response = update_order_status(order_id, status)


    cache_key = f'order_{order_id}'
    cache.delete(cache_key)

    return Response({
        "message": f"Статус заказа #{order_id} обновлён.",
        "data": response
    })

@api_view(['POST'])
@ratelimit(key='ip', rate='5/m', block=True)
def register_view(request):
    """
    Эндпоинт для безопасной регистрации пользователя.
    """
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')


    if not all([username, email, password]):
        return Response({"error": "Все поля обязательны."}, status=400)

    try:
        validate_email(email)
    except ValidationError:
        return Response({"error": "Некорректный email."}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Пользователь с таким именем уже существует."}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Пользователь с таким email уже зарегистрирован."}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()

    logger.info(f"Новый пользователь зарегистрирован: {username} ({email})")

    return Response({"message": "Регистрация прошла успешно."}, status=201)


@api_view(['POST'])
@ratelimit(key='ip', rate='6/m', block=True)
def login_view(request):
    """
    Эндпоинт для безопасного входа пользователя.
    """
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        logger.info(f"Пользователь {username} успешно вошел в систему.")
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "message": "Вход выполнен успешно."
        }, status=200)
    else:
        logger.warning(f"Неудачная попытка входа для пользователя: {username}")
        return Response({"error": "Неверное имя пользователя или пароль."}, status=401)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    """
    Приватный эндпоинт. Доступ только для аутентифицированных пользователей.
    """
    return Response({"message": f"Привет, {request.user.username}! Это защищенный эндпоинт."}, status=200)