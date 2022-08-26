from django.urls import path, include
from rest_framework.routers import DefaultRouter

from advert.views import AdvertViewSet

router = DefaultRouter()
# router.register("advert", AdvertViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
