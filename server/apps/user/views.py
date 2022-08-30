import jwt
from django.http import HttpRequest

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from user.services import send_token_with_mail, send_password_with_email
from user.selectors import get_user_by_id, get_user_by_email
from config.settings.base import SECRET_KEY
from user.api.serializers import (
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    ChangePasswordSerializer,
    EmailSerializer,
    ForgotPasswordSerializer,
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
        send_password_with_email(user, request)

        return Response(
                {"forgot password": "check your email"}, status=status.HTTP_200_OK
        )

class CreateNewPassword(generics.CreateAPIView):
    """
    an endpoint create new password
    """
    serializer_class = ForgotPasswordSerializer

    def post(self, request: HttpRequest) -> Response:
        token = request.GET.get("token")
        data = request.data
        serilaizer = self.get_serializer(data=data)
        serilaizer.is_valid(raise_exception=True)
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user = get_user_by_id(payload["user_id"])
            user.set_password(data['confirm_password'])
            user.save()

            return Response(
                {"password": "Successfully changed"}, status=status.HTTP_200_OK
            )

        except jwt.ExpiredSignatureError as e:
            return Response(
                {"password": "Activation Expired"}, status=status.HTTP_400_BAD_REQUEST
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
        serializer.save()
        user = serializer.user
        send_token_with_mail(user, request)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyEmail(generics.GenericAPIView):
    """
    an endpoint email verification
    """

    def get(self, request: HttpRequest) -> Response:
        token = request.GET.get("token")
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
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
