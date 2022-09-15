from django.urls import include, path

from rest_framework.routers import DefaultRouter

from custom_admin.views import *


router = DefaultRouter()
router.register("advert", AdvertViewSet, basename="advert")
router.register("user", UserViewSet)


urlpatterns = [
    path("admin/", include(router.urls)),
]
