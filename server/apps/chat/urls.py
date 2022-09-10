from django.urls import path

from chat.views import ChatView, ChatDetailAPIView

urlpatterns = [
    path("chat/", ChatView.as_view(), name="chat"),
    path("chat/<int:advert_id>/", ChatDetailAPIView.as_view())
]
