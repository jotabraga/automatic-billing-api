from api.serializers import FileUploadedSerializer
from rest_framework import viewsets, permissions
from api.models import FileUploaded


class FileUploaderViewSet(viewsets.ModelViewSet):
    queryset = FileUploaded.objects.all()
    serializer_class = FileUploadedSerializer
    permission_classes = [permissions.IsAuthenticated]
