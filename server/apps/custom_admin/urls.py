from django.urls import include, path

from rest_framework.routers import DefaultRouter

from custom_admin.views import AdvertView, UserViewSet, AdReportView


router = DefaultRouter()
router.register("advert", AdvertView, basename="advert")
router.register("user", UserViewSet)
router.register("ad_report", AdReportView, basename="ad_report")


urlpatterns = [
    path("admin/", include(router.urls)),
]
