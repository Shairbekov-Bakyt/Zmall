from django.urls import path, include
from rest_framework.routers import DefaultRouter

from advert.api.views.comment_view import CommentView
from advert.api.views.site_view import *
from advert.api.views.advert_view import (
    AdvertViewSet,
    CityListView,
    PremiumAdvertView,
    ContactView,
    AdvertReportView,
    UserAdvertView,
    UserAdvertUpdateView,
    FavAdvertView,
)

router = DefaultRouter()
router.register("advert", AdvertViewSet, basename="advert")
router.register("transaction", TransactionViewSet, basename="transaction")
router.register("favorite", FavoriteAdvertView, basename="favorite_advert")
router.register("promote", PromoteViewSet, basename="promote")
router.register("comment", CommentView, basename="comment")
router.register("feedback", FeedbackView, basename="feedback")
router.register("help", HelpViewSet, basename="help")
router.register("site_link", FooterLinkView, basename="footer")
router.register("help_category", HelpCategoryViewSet, basename="help_category")
router.register("premium_advert", PremiumAdvertView, basename="premium_advert")
router.register("fav_adverts", FavAdvertView, basename="fav_adverts"),

urlpatterns = [
    path("", include(router.urls)),
    path("category/", CategoryView.as_view()),
    path("sub_category/", SubCategoryView.as_view()),
    path("city/", CityListView.as_view()),
    path("FAQ/", FAQListView.as_view()),
    path("favorite/<int:advert_id>/<int:delete>/", FavoriteUpdateDelete.as_view()),
    path("advert_contacts/<int:advert_id>/", ContactView.as_view()),
    path("statistics/", StatisticsView.as_view()),
    path("advert_report/", AdvertReportView.as_view()),
    path("user_advert/", UserAdvertView.as_view()),
    path("user_advert_update/<int:pk>/", UserAdvertUpdateView.as_view()),
    path("feedback_message/", FeedbackMessageView.as_view()),
    path("privacy_policy/", PrivacyPolicyView.as_view()),
]
