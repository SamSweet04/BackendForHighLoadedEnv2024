from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import UploadedFile
from .forms import FileUploadForm
from .serializers import UploadedFileSerializer
from .tasks import process_csv_file

@method_decorator([login_required, csrf_protect], name='dispatch')
class FileUploadView(View):
    def get(self, request):
        form = FileUploadForm()
        return render(request, 'file_processor/upload_form.html', {'form': form})

    def post(self, request):
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            file_instance = UploadedFile.objects.create(user=request.user, file=uploaded_file)
            process_csv_file.delay(file_instance.id)  # Trigger asynchronous processing
            return JsonResponse({'message': 'File uploaded successfully and is being processed.'})
        return JsonResponse({'errors': form.errors}, status=400)


@method_decorator(login_required, name='dispatch')
class FileStatusPageView(View):
    def get(self, request):
        return render(request, 'file_processor/status_page.html')

class UploadStatusAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_files = UploadedFile.objects.filter(user=request.user)
        serializer = UploadedFileSerializer(user_files, many=True)
        return Response(serializer.data)