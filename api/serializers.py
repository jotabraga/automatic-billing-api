from rest_framework import serializers
from api.models import FileUploaded


class FileUploadedSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUploaded
        fields = ["name", "status", "created_at"]
