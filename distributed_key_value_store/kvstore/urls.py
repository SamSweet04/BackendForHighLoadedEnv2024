# kvstore/urls.py
from django.urls import path
from .views import KeyValueView, QuorumKeyValueView

urlpatterns = [
    path('kv/', KeyValueView.as_view(), name='create_key_value'),
    path('kv/<str:key>/', KeyValueView.as_view(), name='get_key_value'),
    path('quorum/kv/', QuorumKeyValueView.as_view(), name='quorum_create_key_value'),
    path('quorum/kv/<str:key>/', QuorumKeyValueView.as_view(), name='quorum_get_key_value'),
]
