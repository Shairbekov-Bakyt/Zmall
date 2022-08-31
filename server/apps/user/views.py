import jwt
from django.http import HttpRequest

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from user.services import send_url_with_mail, send_password_with_email
from user.selectors import get_user_by_email
from user.api.serializers import (
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    ChangePasswordSerializer,
    EmailSerializer,
)


class ForgotPasswordView(generics.CreateAPIView):
    """
    an endpoint forgot password
    """
    serializer_class = EmailSerializer

    def post(self, request, *args, **kwargs):
        email = request.data
        serializer = EmailSerializer(data=email)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']

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
        user.set_password(serializer.data.get("confirm_password"))
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
        serializer.save()
        user = serializer.user
        send_url_with_mail(user, request)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyEmail(generics.GenericAPIView):
    """
    an endpoint email verification
    """

    def get(self, request: HttpRequest) -> Response:
        email = request.GET.get("email")
        try:
            user = get_user_by_email(email)
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
