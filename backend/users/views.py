from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomUserSerializer, RegisterUserSerializer, LoginUserSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

class UserInfoView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user

class UserRegistrationView(CreateAPIView):
    serializer_class = RegisterUserSerializer


class LoginView(APIView):
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)

        #generate tokens
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            response = Response({'user':CustomUserSerializer(user).data},
                                status=status.HTTP_200_OK)
            
            response.set_cookie(key="access_token", value=access_token,
                                httponly=True,
                                secure=True,
                                samesite="Strict")
            
            response.set_cookie(key="refresh_token",
                                value=str(refresh),
                                httponly=True,
                                secure=True,
                                samesite="Strict")
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LogoutView():
    pass