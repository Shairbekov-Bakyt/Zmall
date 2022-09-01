from django.urls import path, include
from rest_framework.routers import DefaultRouter

from advert.views import AdvertViewSet, ImageView

router = DefaultRouter()
router.register("advert", AdvertViewSet, basename='advert')

urlpatterns = [
    path("", include(router.urls)),
    path("advert_image/", ImageView.as_view())

]
