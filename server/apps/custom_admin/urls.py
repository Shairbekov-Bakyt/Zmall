from django.urls import include, path

from rest_framework.routers import DefaultRouter

from custom_admin.views import *


router = DefaultRouter()
router.register("advert", AdvertViewSet, basename="advert")
router.register("favorite", FavoriteAdvertViewSet, basename="favorite_advert")
router.register("comment", CommentViewSet)
router.register("category", CategoryViewSet)
router.register("user", UserViewSet)
router.register("advertImage", AdvertImageViewSet)
router.register("subCategory", SubCategoryViewSet)
router.register("city", CityViewSet)
router.register("promote", PromoteViewSet)
router.register("advertContact", AdvertContactViewSet)
router.register("chat", ChatViewSet)

urlpatterns = [
    path("admin/", include(router.urls)),
]
