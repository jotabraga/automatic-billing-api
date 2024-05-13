from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views

app_name = "api"
router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    path("", views.apiOverview, name="api-overview"),
    path("file-list/", views.fileList, name="file-list"),
    path("file-detail/<str:pk>/", views.fileDetail, name="file-detail"),
    path("file-create/", views.fileCreate, name="file-create"),
]
