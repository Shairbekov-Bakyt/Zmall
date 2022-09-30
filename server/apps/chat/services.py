from django.db.models import Q

from chat.web_socket import pusher_client
from chat.selectors import get_user_channels
from chat.models import Chat


def notify_user(user, ):
    data = {}
    rooms = get_user_channels(user).values_list('id', flat=True)

    for room in rooms:
        data[room] = Chat.objects.filter(to_user=user, is_read=False, room=room).count()

    data['all'] = Chat.objects.filter(to_user=user, is_read=False).count()

    pusher_client.trigger(
        "notification",
        "notificate",
        data,
    )
