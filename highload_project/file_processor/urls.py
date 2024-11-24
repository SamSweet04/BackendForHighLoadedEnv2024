from django.urls import path
from .views import FileUploadView, FileStatusPageView, UploadStatusAPIView

app_name = 'file_processor'

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='upload'),
    path('status/', UploadStatusAPIView.as_view(), name='upload_status'),
    path('status-page/', FileStatusPageView.as_view(), name='status_page'),
]
