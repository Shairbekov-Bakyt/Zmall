from rest_framework import serializers

from chat.models import Chat


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ("id", "from_user", "to_user", "message", "date", "advert", "file")

    def create(self, validated_data):
        chat = Chat.objects.create(**validated_data)
        chat.save()
        self.chat = chat
        return self.chat


class ChatListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ("id", "from_user", "message", "date", "advert")