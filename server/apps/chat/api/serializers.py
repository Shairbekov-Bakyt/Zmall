from rest_framework import serializers

from chat.models import Chat, Room
from user.models import CustomUser as User
from advert.models import Advert


class UserForChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name")


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ("id", "message", "room", "from_user", "to_user", "date", "file")
        extra_kwargs = {
            "file": {"required": False},
            "message": {"required": False}}


class ChatListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["owner"] = {}
        data["user"] = {}

        advert_id = instance.advert.id

        chat = Chat.objects.filter(room=instance).last()
        if chat is not None:

            data["message"] = chat.message
            data["date"] = chat.date

        data["advert_id"] = advert_id
        data["advert"] = Advert.objects.get(pk=advert_id).name

        data["owner"]["id"] = instance.owner.id
        data["owner"]["first_name"] = instance.owner.first_name
        data["owner"]["last_name"] = instance.owner.last_name
        data["user"]["id"] = instance.user.id
        data["user"]["first_name"] = instance.user.first_name
        data["user"]["last_name"] = instance.user.last_name
        return data
