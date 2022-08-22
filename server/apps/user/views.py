import jwt
from django.conf import settings
from django.http import HttpRequest

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from user.api.serializers import MyTokenObtainPairSerializer, RegisterSerializer
from user.services import send_token_with_mail
from user.selectors import get_user_by_id

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request: HttpRequest) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = serializer.user
        send_token_with_mail(user, request)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user =  get_user_by_id(payload['user_id'])
            if not user.is_activate:
                user.is_activate = True
                user.save()

            return Response({"email": "Successfully activated"}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as e:
            return Response({"email": "Activation Expired"}, status=status.HTTP_400_BAD_REQUEST)
