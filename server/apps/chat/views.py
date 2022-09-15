from django.db.models import Q

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from chat.web_socket import pusher_client
from chat.api.serializers import ChatSerializer, ChatListSerializer
from chat.models import Chat, Room


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = ChatListSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post"]

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response([])

        obj = Room.objects.filter(Q(owner=request.user) | Q(user=request.user))
        serializer =self.get_serializer(obj, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk, *args, **kwargs):
        room = Room.objects.get(pk=pk)
        obj = Chat.objects.filter(Q(to_user=request.user, room=room) | Q(from_user=request.user, room=room))
        serializer = ChatSerializer(obj, many=True)
        return Response({'message': serializer.data, 'advert_name': room.advert.name, 'advert_price': room.advert.start_price})

    def create(self, request, *args, **kwargs):
        try:
            obj = Room.objects.get(
                owner=request.data['owner'],
                user=request.data['user'],
                advert=request.data['advert'])
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
            Room.objects.get(pk=request.data['room'])
        except:
            Room.objects.create()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        chat = serializer.save()
        pusher_client.trigger(f"{chat.room.id}", "message_create",
                      {
                          "message": chat.message,
                          "from_user": chat.from_user.get_full_name(),
                          "to_user": chat.to_user.get_full_name(),
                          "date": str(chat.date),
                      })
        return Response({"message": serializer.data, "advert_name": chat.room.advert.name, "advert_price": chat.room.advert.start_price})