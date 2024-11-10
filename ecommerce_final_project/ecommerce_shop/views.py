from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import viewsets
from .models import User, Product, Category, Order, OrderItem, ShoppingCart, CartItem, Payment, Review, Wishlist, WishlistItem
from .serializers import (
    UserSerializer, ProductSerializer, CategorySerializer, OrderSerializer, OrderItemSerializer,
    ShoppingCartSerializer, CartItemSerializer, PaymentSerializer, ReviewSerializer, WishlistSerializer, WishlistItemSerializer
)


class CachedProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        cache_key = 'products'
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 15)  # 15 minutes
        return response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category')
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        cache_key = 'products_list'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 10)
        return response

    def retrieve(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        cache_key = f'product_{product_id}'
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 10)
        return response

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('user').prefetch_related('orderitem_set')
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.select_related('user')
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
    queryset = Wishlist.objects.select_related('user')
    serializer_class = WishlistSerializer

class WishlistItemViewSet(viewsets.ModelViewSet):
    queryset = WishlistItem.objects.select_related('wishlist', 'product')
    serializer_class = WishlistItemSerializer
