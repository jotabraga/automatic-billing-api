from django_filters.rest_framework import DjangoFilterBackend
from api.serializers import FileUploadedSerializer, CSVFileSerializer
from api.models import FileUploaded
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.request import Request
from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .tasks import process_large_csv
from rest_framework import status


@api_view(["GET"])
def apiOverview(request):
    api_urls = {
        "List": "/file-list/",
        "Detail View": "/file-detail/<str:pk>/",
        "Create": "/file-upload/",
        "Update": "/file-update/<str:pk>/",
        "Delete": "/file-delete/<str:pk>/",
    }
    return Response(api_urls)


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
def fileProcessing(request: Request, format=None):
    csv_file = request.FILES["file"]
    file_name = csv_file.name

    process_large_csv(csv_file)

    # serializer = CSVFileSerializer(data=request.data)
    # if serializer.is_valid():
    #     file = serializer.validated_data["file"]

    # else:
    #     saveFileUploadRecord(file.name, "fail")

    saveFileRecord = saveFileUploadRecord(file_name, "success")

    return Response(
        {
            "name": csv_file.name,
            "status": "success",
            "created_at": saveFileRecord["created_at"],
        },
        status=status.HTTP_200_OK,
    )


def saveFileUploadRecord(filename, status):

    fileUploadserializer = FileUploadedSerializer(
        data={"name": filename, "status": status}
    )
    if fileUploadserializer.is_valid():
        fileUploadserializer.save()
        return fileUploadserializer.data
