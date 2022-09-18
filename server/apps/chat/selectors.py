from django.db.models import Q

from chat.models import Chat, Room


def get_user_channels(user):
    return Room.objects.filter(Q(owner=user) | Q(user=user))


def get_user_messages_in_channels(user, channel):
    return Chat.objects.filter(
        Q(to_user=user, room=channel) | Q(from_user=user, room=channel)
    )
