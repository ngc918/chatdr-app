import jwt
from django.conf import settings
from datetime import datetime
from .models import CustomUser
from rest_framework.authentication import BaseAuthentication

class Authentication(BaseAuthentication):
    def authenticate(self, request):
        data = self.validate_request(request.headers)
        if not data:
            return None, None
        return self.get_user(data["user_id"]), None
    
    def get_user(self, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
            return user
        except Exception:
            return None
        
    def validate_request(self, headers):
        authorization = headers.get("Authorization", None)
        if not authorization:
            return None
        token = headers["Authorization"][7:]
        decoded_data = Authentication.verify_token(token)

        if not decoded_data:
            return None
        
        return decoded_data
    
    @staticmethod
    def verify_token(token):
        try:
            decode_data = jwt.decode(token, settings.SECRET_KEY, algorithm="")
        except Exception:
            return None
        
        # checks if token is expired
        exp = decode_data["exp"]

        if datetime.now().timestamp() > exp:
            return None
        
        return decode_data