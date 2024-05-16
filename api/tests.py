from django.test import TestCase
from .models import FileUploaded


class FileUploadModelTest(TestCase):
    def test_file_upload_model_exists(self):
        uploadedFiles = FileUploaded.objects.count()
        self.assertEqual(uploadedFiles, 0)
