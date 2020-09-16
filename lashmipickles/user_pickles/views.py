from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import authenticate, login, logout
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication, JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, status
from rest_framework_jwt.utils import jwt_decode_handler
from rest_framework.response import Response
from .seriailizer import GetUserSerializer
from .models import User
import json

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER    

# Create your views here.

class UserLogin(viewsets.ViewSet):
    # serializer_class = GetUserSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        email = request.data['email']
        password = request.data['password']

        user = authenticate(email=email, password=password)
        if user is not None:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            return Response({"message": "User loged in sucessfulyy", "token": jwt_token})
        else:
            return Response({"message": "Invalid creditionals"})

class UserRegister(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = GetUserSerializer
    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        print(request.data)
        data = json.loads(json.dumps(request.data))
        data['password'] = make_password(data['password'])
        serializer = self.serializer_class(data= data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            name = serializer.data.get('username')
            return Response({'message': name})

        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )