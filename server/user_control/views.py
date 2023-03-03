import jwt
from django.contrib.auth import authenticate
from django.conf import settings
from datetime import datetime, timedelta
from .models import CustomUser, Jwt
import random
import string
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer, RegisterSerializer, RefreshSerializer
from .authentication import Authentication

# Create your views here.

def get_random(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def access_token(payload):
    return jwt.encode(
        {"exp": datetime.now() + timedelta(minutes=5), **payload},
        settings.SECRET_KEY,
        algorithm="HS256"
    )

def refresh_token():
    return jwt.encode(
        {"exp": datetime.now() + timedelta(days=365), "data": get_random(10)},
        settings.SECRET_KEY,
        algorithm="HS256"
    )

def decodeJWT():
    decoded = jwt.decode(key=settings.SECRET_KEY)
    if decoded:
        try:
            return
        except:
            return None

class LoginView(APIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username = serializer.validated_data['username'],
            password = serializer.validated_data['password'])
        
        if not user:
          return Response({"error": "Invalid username and/or password"}, status="400")
        
        Jwt.objects.filter(user_id=user.id).delete()

        access = access_token({"user_id": user.id})
        refresh = refresh_token()

        Jwt.objects.create(
            user_id=user.id, access=access.encode().decode(), refresh=refresh.encode().decode()
        )

        return Response({"access": access, "refresh": refresh})

class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        CustomUser.objects._create_user(**serializer.validated_data)

        return Response({"success": "User created."}, status=201)
    
class RefreshView(APIView):
    serializer_class = RefreshSerializer

    def post(self, request): 
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try: 
            active_jwt = Jwt.objects.get(
                refresh = serializer.validated_data["refresh"]
            )
        except Jwt.DoesNotExist:
            return Response({"error": "refresh token not found"}, status="400")
        if not Authentication.verify_token(serializer.validated_data["refresh"]):
            return Response({"error": "Token is invalid or has expired"})
        
        access = access_token({"user_id": active_jwt.user.id})
        refresh = refresh_token()

        active_jwt.access = access.encode().decode()
        active_jwt.refresh = refresh.encode().decode()
        active_jwt.save()
        
