from datetime import datetime
from doctest import REPORT_CDIFF
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.conf import settings
from django.middleware import csrf

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .utils import get_tokens, timedelta_to_seconds
from .serializers import UserSerializer

from todo.models import TodoList
from todo.serializers import TodoListSerializer

# Create your views here.
@api_view(["GET"])
def get_csrf(request):
    response = Response()
    csrf_token = csrf.get_token(request)
    response["X-CSRFToken"] = csrf_token
    response.data = {"status": "success"}
    return response


class SignUp(CreateAPIView):
    Permission_classes = [AllowAny,]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class Login(APIView):
    permission_classes = [AllowAny,]

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        response = Response()
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"msg": "Invalid username or password."}, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_active:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        tokens = get_tokens(user)
        refresh_expires = timedelta_to_seconds(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'])
        access_expires = timedelta_to_seconds(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'])
        # response.set_cookie(
        #     key= settings.SIMPLE_JWT["AUTH_COOKIE"],
        #     value= tokens["access"],
        #     expires= access_expires,
        #     secure= settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        #     samesite= settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
        #     httponly= settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],  
        # )
        # response.set_cookie(
        #     key= settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
        #     value= tokens["refresh"],
        #     expires= refresh_expires,
        #     secure= settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        #     samesite= settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
        #     httponly= settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],  
        # )

        response.data = {
            "status": "success",
            "msg": "Login Successfull.",
            "tokens": {"refresh": tokens["refresh"], "access": tokens["access"]},
            "access_expires": access_expires,
            "refresh_expires": refresh_expires,
        }
        response.status_code = status.HTTP_200_OK
        if TodoList.objects.filter(owner=user).exists():
            return response

        todo_list = TodoList(owner=user)
        todo_list.save()
        return response

class LogoutView(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request):
        print("request: ", request)
        response = Response()
        print("response before deleting cookie", response.cookies)
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        response.data = {
            "status": "success",
            "msg": "User logout successfully"
        }
        response.status_code = status.HTTP_200_OK
        print("response after deleting cookie", response.cookies)
        return response

class GetCurrentUser(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)