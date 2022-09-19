from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .settings import base

schema_view = get_schema_view(
    openapi.Info(
        title="Zeon Mall API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
API_PREFIX = 'api/v1/'
urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    path("admin/", admin.site.urls),
    path(f"{API_PREFIX}user/", include("user.urls")),
    path(f"{API_PREFIX}", include("advert.urls")),
    path(f"{API_PREFIX}", include("chat.urls")),
    path(f"{API_PREFIX}", include("custom_admin.urls")),
    path(f"{API_PREFIX}social_auth/", include("social_auth.urls")),
]

urlpatterns += static(base.MEDIA_URL, document_root=base.MEDIA_ROOT)
