from rest_framework.viewsets import ModelViewSet
from .serializers import FileUpload, FileUploadSerializer

# Create your views here.

class FileUploadView(ModelViewSet):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
