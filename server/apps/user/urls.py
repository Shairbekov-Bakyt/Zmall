from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView


from user.views import (
    MyObtainTokenPairView,
    RegisterView,
    VerifyEmail,
    ChangePasswordView,
    ForgotPasswordView,
)


urlpatterns = [
    path("login/", MyObtainTokenPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="auth_register"),
    path("activation/", VerifyEmail.as_view(), name="email-verify"),
    path("change_password/", ChangePasswordView.as_view(), name="user_change_password"),
    path("forgot_password/", ForgotPasswordView.as_view(), name='forgot_user'),
]
