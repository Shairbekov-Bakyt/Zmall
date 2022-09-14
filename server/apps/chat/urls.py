from django.urls import path, include

from rest_framework.routers import DefaultRouter

from chat.views import RoomViewSet, ChatCreateView

router = DefaultRouter()
router.register('chat_room', RoomViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("message/", ChatCreateView.as_view()),
]
