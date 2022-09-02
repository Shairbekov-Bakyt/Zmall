from django.urls import path, include
from rest_framework.routers import DefaultRouter

from advert.views.advert_views import AdvertViewSet
from advert.views.promote_views import PromoteViewSet
from advert.views.category_views import CategoryView

router = DefaultRouter()
router.register("advert", AdvertViewSet, basename='advert')
router.register("promote", PromoteViewSet, basename='promote')

urlpatterns = [
    path("", include(router.urls)),
    path("category/", CategoryView.as_view())
]
