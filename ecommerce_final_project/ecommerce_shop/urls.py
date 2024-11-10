from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, ProductViewSet, CategoryViewSet, OrderViewSet, OrderItemViewSet,
    ShoppingCartViewSet, CartItemViewSet, PaymentViewSet, ReviewViewSet, WishlistViewSet, WishlistItemViewSet
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
]
