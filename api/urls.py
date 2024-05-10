from rest_framework.routers import DefaultRouter
from api.views import FileUploaderViewSet

app_name = "api"
router = DefaultRouter(trailing_slash=False)
router.register("file", FileUploaderViewSet)
urlpatterns = router.urls
