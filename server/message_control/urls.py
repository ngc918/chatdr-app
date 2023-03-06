from rest_framework.routers import DefaultRouter
from .views import FileUploadView
from django.urls import path, include

router = DefaultRouter(trailing_slash=False)

router.register("file-upload", FileUploadView)

urlpatterns = [
    path("", include(router.urls))
]
