from rest_framework.serializers import ModelSerializer
from .models import FileUpload

class FileUploadSerializer(ModelSerializer):
    
    class Meta:
        model = FileUpload
        fields = "__all__"