from django.db.models import Q

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from chat.web_socket import pusher_client
from chat.api.serializers import ChatSerializer, ChatListSerializer
from chat.models import Chat, Room
from chat.selectors import (
    get_user_channels,
    get_user_messages_in_channels,
)


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = ChatListSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post"]

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response([])

        obj = get_user_channels(request.user)
        serializer = self.get_serializer(obj, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk, *args, **kwargs):
        room = Room.objects.get(pk=pk)
        obj = get_user_messages_in_channels(request.user, room)
        serializer = ChatSerializer(obj, many=True)
        response_data = {
            "messages": serializer.data,
            "advert_id": room.advert.id,
            "advert": room.advert.name,
            "to_user": {
                "id": room.user.id,
                "first_name": room.user.first_name,
                "last_name": room.user.last_name,
            },
            "from_user": {
                "id": room.owner.id,
                "first_name": room.owner.first_name,
                "last_name": room.user.last_name,
            },
        }
        return Response(response_data)

    def create(self, request, *args, **kwargs):
        try:
            obj = Room.objects.get(
                owner=request.data["owner"],
                user=request.data["user"],
                advert=request.data["advert"],
            )
            serializer = self.get_serializer(obj)
            return Response(serializer.data)

        except:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class ChatCreateView(CreateAPIView):
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            Room.objects.get(pk=request.data["room"])
        except:
            Room.objects.create()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        chat = serializer.save()

        data = {
            "message": chat.message,
            "from_user": chat.from_user.id,
            "to_user": chat.to_user.id,
            "date": str(chat.date),
        }

        if chat.file:
            data["file"] = chat.file.url

        pusher_client.trigger(f"{chat.room.id}", "message_create", data)
        response_data = {
            "message": serializer.data,
            "advert_name": chat.room.advert.name,
            "advert_price": chat.room.advert.start_price,
        }
        return Response(response_data)
