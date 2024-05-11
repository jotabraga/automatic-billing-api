from django_filters.rest_framework import DjangoFilterBackend
from api.serializers import FileUploadedSerializer
from rest_framework import viewsets, permissions
from api.models import FileUploaded
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.request import Request
from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view


@api_view(http_method_names=["POST"])
class FileUploaderViewSet(viewsets.ModelViewSet):
    queryset = FileUploaded.objects.all()
    serializer_class = FileUploadedSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status"]
    ordering = ["created_at"]
