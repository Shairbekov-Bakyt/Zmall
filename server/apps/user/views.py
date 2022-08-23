import jwt
from django.http import HttpRequest

from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from user.api.serializers import MyTokenObtainPairSerializer, RegisterSerializer, ChangePasswordSerializer
from user.services import send_token_with_mail
from user.selectors import get_user_by_id
from config.settings.base import SECRET_KEY


class ChangePasswordView(generics.UpdateAPIView):
    """
    an endpoint change password
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.data.get('new_password'))
        user.save()
        return Response({"password": "password change successfully"}, status=status.HTTP_200_OK)


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
