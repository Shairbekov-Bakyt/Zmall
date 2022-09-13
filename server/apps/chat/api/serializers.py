from rest_framework import serializers

from chat.models import Chat, Room
from advert.models import Advert


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'

    def create(self, validated_data):
        chat = Chat.objects.create(**validated_data)
        chat.save()
        self.chat = chat
        return self.chat


class ChatListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        advert_id = instance.advert.id

        chat = Chat.objects.filter(room=instance).last()

        username = chat.to_user if instance.user == chat.from_user else chat.from_user


        if chat is not None:
            data['message'] = chat.message
            data['date'] = chat.date

        data['username'] = username.get_full_name()
        data['advert_id'] = advert_id
        data['advert'] = Advert.objects.get(pk=advert_id).name

        return data
