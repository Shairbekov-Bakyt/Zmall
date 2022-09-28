from django.shortcuts import get_object_or_404
from django.http import HttpRequest

import jwt, json
from decouple import config
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from user.services import send_code_with_mail, send_password_with_email
from user.models import CustomUser as User
from user.selectors import get_user_by_email, get_user_by_id
from user.api.serializers import (
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    UserLoginSerializer,
    EmailSerializer,
    ChangeUserInfoSerializer,
    VerifyEmailCodeSerializer,
)


class LoginCreateView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        if not request.data:
            return Response({'Error': "Please provide username/password"}, status="400")

        email = request.data['email']
        password = request.data['password']
        user = get_object_or_404(User, email=email)
        if not user.check_password(password):
            return Response({'Error': "Invalid username/password"}, status="400")

        if not user:
            return Response(
                json.dumps({'Error': "Invalid credentials"}),
                status=400,
                content_type="application/json"
            )

        payload = {
            'id': user.id,
            'email': user.email,
        }
        jwt_token = {'token': jwt.encode(payload, config("SECRET_KEY"))}

        return Response(
            json.dumps(jwt_token),
            status=200,
            content_type="application/json"
        )


class ChangeUserInfoView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = User.objects.all()
    serializer_class = ChangeUserInfoSerializer

    def get_object(self):
        return self.request.user


class ForgotPasswordView(generics.CreateAPIView):
    """
    an endpoint forgot password
    """

    serializer_class = EmailSerializer

    def post(self, request, *args, **kwargs):
        email = request.data
        serializer = EmailSerializer(data=email)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        user = get_user_by_email(email)
        send_password_with_email(user)

        return Response(
            {"forgot password": "check your email"}, status=status.HTTP_200_OK
        )


class MyObtainTokenPairView(TokenObtainPairView):
    """
    an endpoint login
    """

    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.GenericAPIView):
    """
    an endpoint registration
    """

    serializer_class = RegisterSerializer

    def post(self, request: HttpRequest) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_code_with_mail(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyEmail(generics.GenericAPIView):
    """
    an endpoint email verification
    """

    def get(self, request: HttpRequest) -> Response:
        token = request.GET.get("token")
        try:
            payload = jwt.decode(token, config('SECRET_KEY'), algorithms=["HS256"])
            user = get_user_by_id(payload["user_id"])
            if not user.is_active:
                user.is_active = True
                user.save()

            return Response(
                {"email": "Successfully activated"}, status=status.HTTP_200_OK
            )

        except jwt.ExpiredSignatureError as e:
            return Response(
                {"email": "Activation Expired"}, status=status.HTTP_400_BAD_REQUEST
            )


class CheckActivationCode(generics.CreateAPIView):
    serializer_class = VerifyEmailCodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"status": "activate"})
