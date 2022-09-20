from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import GoogleSocialAuthSerializer, FacebookSocialAuthSerializer
from google.oauth2 import id_token
from google.auth.transport import requests
from decouple import config

from user.models import CustomUser


class GoogleSocialAuthView(GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """

        POST with "auth_token"

        Send an idtoken as from google to get user information

        """
        user = id_token.verify_oauth2_token(
            request.data["auth_token"], requests.Request(), config("GOOGLE_CLIENT_ID")
        )
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data)["auth_token"]

        user_by_email = CustomUser.objects.get(email=data["email"])
        tokens = user_by_email.tokens()
        data = {
            "email": user_by_email.email,
            "first_name": user_by_email.first_name,
            "last_name": user_by_email.last_name,
            "user_id": user_by_email.id,
            "phone_number": user_by_email.phone_number,
            **tokens,
        }

        return Response(data, status=status.HTTP_200_OK)


class FacebookSocialAuthView(GenericAPIView):

    serializer_class = FacebookSocialAuthSerializer

    def post(self, request):
        """

        POST with "auth_token"

        Send an access token as from facebook to get user information

        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data)["auth_token"]
        return Response(data, status=status.HTTP_200_OK)
