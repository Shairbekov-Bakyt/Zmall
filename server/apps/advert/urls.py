from django.urls import path, include
from rest_framework.routers import DefaultRouter

from advert.views.advert_views import AdvertViewSet, CityListView, PremiumAdvertView
from advert.views.promote_views import PromoteViewSet
from advert.views.category_views import CategoryView
from advert.views.favorite_view import FavoriteAdvertView
from advert.views.subcategory_views import SubCategoryView


router = DefaultRouter()
router.register("advert", AdvertViewSet, basename="advert")
router.register("favorite", FavoriteAdvertView, basename="favorite_advert")
router.register("promote", PromoteViewSet, basename="promote")


urlpatterns = [
    path("", include(router.urls)),
    path("category/", CategoryView.as_view()),
    path("sub_category/", SubCategoryView.as_view()),
    path("city/", CityListView.as_view()),
    path("premium_advert/", PremiumAdvertView.as_view())
]
