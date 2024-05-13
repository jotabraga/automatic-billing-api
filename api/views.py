from django_filters.rest_framework import DjangoFilterBackend
from api.serializers import FileUploadedSerializer
from rest_framework import viewsets, permissions
from api.models import FileUploaded
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.request import Request
from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import csv
from .tasks import my_task


@api_view(["GET"])
def apiOverview(request):
    api_urls = {
        "List": "/file-list/",
        "Detail View": "/file-detail/<str:pk>/",
        "Create": "/file-create/",
        "Update": "/file-update/<str:pk>/",
        "Delete": "/file-delete/<str:pk>/",
    }
    result = my_task(2, 3)

    return Response({result})


@api_view(["GET"])
def fileList(_request: Request):
    files = FileUploaded.objects.all()
    serializer = FileUploadedSerializer(files, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def fileDetail(_request, pk):
    file = FileUploaded.objects.get(id=pk)
    serializer = FileUploadedSerializer(file, many=False)
    response = serializer.data
    return Response(response)


@api_view(["POST"])
def fileCreate(request: Request):
    serializer = FileUploadedSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)
