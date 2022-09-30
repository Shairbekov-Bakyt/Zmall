from django.db.models import Q

from chat.models import Chat, Room
from user.models import CustomUser as User


def get_user_channels(user):
    return Room.objects.filter(Q(owner=user) | Q(user=user))


def get_user_messages_in_channels(user, channel):
    return Chat.objects.filter(
        Q(to_user=user, room=channel) | Q(from_user=user, room=channel)
    )


def get_all_messages_notification(user: User):
    notification: int = Chat.objects.filter(is_read=False, to_user=user).count()
    return notification
