from django.test import TestCase
from rest_framework.test import APITestCase
from .models import FileUploaded
from .serializers import FileUploadedSerializer
from rest_framework import status
from django.urls import reverse


class FileUploadModelTest(TestCase):
    def testFileModelExists(self):
        uploaded_files = FileUploaded.objects.count()

        self.assertEqual(uploaded_files, 0)

    def testFileModelHasStringRepresentation(self):
        file_record = {"name": "test", "status": "success"}
        fileUploadserializer = FileUploadedSerializer(data=file_record)
        if fileUploadserializer.is_valid():
            instance = fileUploadserializer.save()
        instance_from_db = FileUploaded.objects.get(pk=instance.pk)

        self.assertEqual(str(instance_from_db), file_record["name"])


class TestApiOverview(APITestCase):
    def setUp(self):
        self.api_urls = {
            "List": "/file-list/",
            "Detail View": "/file-detail/<str:pk>/",
            "Create": "/file-upload/",
            "Update": "/file-update/<str:pk>/",
            "Delete": "/file-delete/<str:pk>/",
        }

    def test_api_overview(self):
        response = self.client.get(reverse("api:api-overview"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.api_urls)


class TestApiGetFileRecords(APITestCase):
    def setUp(self):
        files = [{}]

    def test_api_overview(self):
        response = self.client.get(reverse("api:api-overview"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.api_urls)
