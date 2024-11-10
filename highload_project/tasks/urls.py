from django.urls import path
from tasks import views as task_views

urlpatterns = [
    path('send-email/', task_views.create_email_view, name='send_email')
]
