from django.urls import path

from .views import UploadAudio

urlpatterns = [
    path('upload-audio/', UploadAudio.as_view(), name='upload_audio'),
]