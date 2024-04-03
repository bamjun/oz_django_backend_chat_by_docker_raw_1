from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from rest_framework.permissions import IsAuthenticated

import pdb
def login_page(request):
    return render(request, 'login.html')

def signup_page(request):
    return render(request,'signup.html')

# api/v1/users/login
class Login(APIView):
    def post(self, request):
        print(request.data)

        email = request.data['email']
        password = request.data['password']

        if not email or not password:
            raise ParseError()
        
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            data = UserSerializer(user)

            return Response(data.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
    
class Signup(APIView):
    def post(self, request):
        User.objects.create_user(email=request.data['email'], password=request.data['password'], nickname=request.data['nickname'])

        return Response(request.data, status=status.HTTP_201_CREATED)
        