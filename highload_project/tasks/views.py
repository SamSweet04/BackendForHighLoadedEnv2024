# views.py
import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.cache import cache_page
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from .models import Email
from .tasks import send_email_task
from .throttles import RoleBasedThrottle


@method_decorator(csrf_protect, name='dispatch')  # Добавлена CSRF защита
class SendEmailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Только авторизованные пользователи
    throttle_classes = [RoleBasedThrottle, ScopedRateThrottle]
    throttle_scope = 'send_email'

    def post(self, request, *args, **kwargs):
        try:
            if request.content_type == "application/x-www-form-urlencoded":
                recipient = request.POST.get('recipient')
                subject = request.POST.get('subject')
                body = request.POST.get('body')
            else:
                data = json.loads(request.body)
                recipient = data.get('recipient')
                subject = data.get('subject')
                body = data.get('body')

            if not (recipient and subject and body):
                return Response({'error': 'All fields are required!'}, status=400)

            # Создаем объект Email с валидацией
            email = Email(
                recipient=recipient,
                subject=subject,
                body=body
            )
            email.full_clean()  # Валидация модели
            email.save()

            # Отправляем email через Celery
            send_email_task.delay(recipient, subject, body)

            return Response({'message': 'Email is being sent!'}, status=202)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON data!'}, status=400)
        except ValidationError as e:
            return Response({'error': e.messages}, status=400)

    def get(self, request, *args, **kwargs):
        return render(request, 'tasks/email_form.html')

@cache_page(60 * 15)
def home(request):
    return HttpResponse("Welcome to the High Load Project!")
