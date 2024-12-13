import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import UploadedFile

class FileProcessorTests(APITestCase):

    def setUp(self):
        # Create a test user and obtain JWT token
        self.user = User.objects.create_user(username='admin', password='admin')
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'admin',
            'password': 'admin'
        })
        self.access_token = response.data['access']

    def test_file_upload(self):
        # Test file upload functionality
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        temp_file = tempfile.NamedTemporaryFile(suffix=".csv")
        temp_file.write(b"header1,header2\nrow1,row2")  # Mock CSV content
        temp_file.seek(0)

        response = self.client.post(
            reverse('file_processor:upload'),
            {'file': SimpleUploadedFile(temp_file.name, temp_file.read())},
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UploadedFile.objects.count(), 1)

    def test_upload_status(self):
        # Test upload status retrieval
        UploadedFile.objects.create(
            user=self.user,
            file="uploads/test.csv",
            status="Processing"
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(reverse('file_processor:upload_status'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_file_upload_permission(self):
        # Test access restriction for unauthenticated users
        temp_file = tempfile.NamedTemporaryFile(suffix=".csv")
        temp_file.write(b"header1,header2\nrow1,row2")  # Mock CSV content
        temp_file.seek(0)

        response = self.client.post(
            reverse('file_processor:upload'),
            {'file': SimpleUploadedFile(temp_file.name, temp_file.read())},
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_rate_limiting(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        for _ in range(10):  # Exceed the throttling limit
            response = self.client.get(reverse('file_processor:upload_status'))
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_invalid_file_type(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        temp_file = tempfile.NamedTemporaryFile(suffix=".exe")
        temp_file.write(b"Fake binary content")
        temp_file.seek(0)

        response = self.client.post(
            reverse('file_processor:upload'),
            {'file': SimpleUploadedFile(temp_file.name, temp_file.read())},
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

