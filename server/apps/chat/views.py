from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from chat.api.serializers import ChatSerializer
from chat.web_socket import pusher_client
from chat.models import Chat


class ChatView(GenericAPIView):
    """
    an endpoint messanger with customer
    """
    serializer_class = ChatSerializer

    def post(self, request, *args, **kwargs) -> Response:
        data = request.data
        seralizer = self.get_serializer(data=data)
        seralizer.is_valid(raise_exception=True)
        seralizer.save()
        chat = seralizer.chat
        pusher_client.trigger(
            "my_channel",
            str(chat.id),
            {
                "message": chat.message,
                "date": str(chat.date),
                "from_user": chat.from_user.get_full_name(),
                "to_user": chat.to_user.get_full_name(),
            },
        )
        return Response(seralizer.data)
