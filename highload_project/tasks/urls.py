from django.urls import path, include

from tasks.views import home

from tasks.views import SendEmailView

urlpatterns = [
    path('', home, name='home'),
    path('send-email/', SendEmailView.as_view(), name='send_email'),
]
