from django.shortcuts import render
from django.http import JsonResponse
from .models import Email
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_email_view(request):
    if request.method == 'POST':
        recipient = request.POST.get('recipient')
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        email = Email.objects.create(recipient=recipient, subject=subject, body=body)
        return JsonResponse({'status': 'Email is being sent'})