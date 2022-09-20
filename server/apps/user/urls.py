from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView


from user.views import (
    MyObtainTokenPairView,
    RegisterView,
    VerifyEmail,
    ForgotPasswordView,
    ChangeUserInfoView,
    CheckActivationCode,
)


urlpatterns = [
    path("login/", MyObtainTokenPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("change/info/", ChangeUserInfoView.as_view(), name="user_update"),
    path("check/activation/code/", CheckActivationCode.as_view(), name="user_activate"),
    path("register/", RegisterView.as_view(), name="auth_register"),
    path("activation/", VerifyEmail.as_view(), name="email-verify"),
    path("forgot/password/", ForgotPasswordView.as_view(), name="forgot_user"),
]
