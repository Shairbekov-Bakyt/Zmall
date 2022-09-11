from itertools import chain

from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from chat.api.serializers import ChatSerializer, ChatListSerializer
from chat.web_socket import pusher_client
from chat.models import Chat
from chat.selectors import get_messages_from_user, get_messages_from_advert_id, get_messages_to_user


class ChatView(GenericAPIView):
    """
    an endpoint messanger with customer message detail
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer

    def post(self, request, *args, **kwargs) -> Response:
        data = request.data
        seralizer = self.get_serializer(data=data)
        seralizer.is_valid(raise_exception=True)
        seralizer.save()
        chat = seralizer.chat
        pusher_client.trigger(
            f"{chat.advert.id}-{chat.from_user}",
            str(chat.id),
            {
                "message": chat.message,
                "date": str(chat.date),
                "from_user": chat.from_user.get_full_name(),
                "to_user": chat.to_user.get_full_name(),
            },
        )
        return Response(seralizer.data)


    def get(self, request):
        messages_from_user = get_messages_from_user(request)
        messages_to_user = get_messages_to_user(request)
        obj = list(chain(messages_to_user, messages_from_user))
        serializer = self.get_serializer(obj, many=True)
        return Response(serializer.data)


class ChatDetailAPIView(RetrieveAPIView):
    """an endpoint list messages"""
    queryset = Chat.objects.all()
    serializer_class = ChatListSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, advert_id, *args, **kwargs):
        messages_from_advert_id = get_messages_from_advert_id(request, advert_id)
        serializer = self.get_serializer(messages_from_advert_id, many=True)
        return Response(serializer.data)


