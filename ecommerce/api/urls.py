from django.urls import path
from .views import (
    ProductListAPIView, ProductDetailAPIView,
    CategoryListAPIView, CategoryDetailAPIView,
    OrderListAPIView, OrderDetailAPIView, UserListAPIView, UserDetailAPIView, RegisterAPIView, LoginAPIView
)

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('orders/', OrderListAPIView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
]
