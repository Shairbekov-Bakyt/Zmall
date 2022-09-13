from django.db.models import Q

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from chat.api.serializers import ChatSerializer, ChatListSerializer
from chat.models import Chat, Room


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = ChatListSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

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