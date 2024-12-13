from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    UserViewSet, ProductViewSet, CategoryViewSet, OrderViewSet, OrderItemViewSet,
    ShoppingCartViewSet, CartItemViewSet, PaymentViewSet, ReviewViewSet, WishlistViewSet, WishlistItemViewSet,
    create_order_view, get_order_view, update_order_view, register_view, login_view, protected_view
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)
router.register(r'shopping-carts', ShoppingCartViewSet)
router.register(r'cart-items', CartItemViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'wishlists', WishlistViewSet)
router.register(r'wishlist-items', WishlistItemViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('create-order/', create_order_view, name='create-order'),
    path('get-order/<str:order_id>/', get_order_view, name='get-order'),
    path('update-order/<str:order_id>/', update_order_view, name='update-order'),
    path('auth/register/', register_view, name='register'),
    path('auth/login/', login_view, name='login'),
    path('auth/protected/', protected_view, name='protected'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
