import jwt
from django.http import HttpRequest
from decouple import config

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from phonenumber_field.modelfields import PhoneNumberField, validate_international_phonenumber

from user.services import send_code_with_mail, send_password_with_email
from user.models import CustomUser as User
from user.selectors import get_user_by_email, get_user_by_id
from user.api.serializers import (
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    ChangePasswordSerializer,
    EmailSerializer,
    ChangeUserInfoSerializer,
    VerifyEmailCodeSerializer,
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


class ChangePasswordView(generics.UpdateAPIView):
    """
    an endpoint change password
    """

    serializer_class = ChangePasswordSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_object(self):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.data.get("new_password"))
        user.save()
        return Response(
            {"password": "password change successfully"}, status=status.HTTP_200_OK
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
