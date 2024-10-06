from django.urls import path
from .views import post_list_view, post_detail_view

urlpatterns = [
    path('posts/', post_list_view, name='post_list'),
    path('post/<int:post_id>/', post_detail_view, name='post_detail'),
]
