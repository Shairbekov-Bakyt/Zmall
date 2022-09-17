from rest_framework import serializers

from advert.models import Promote


class PromoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promote
        fields = "__all__"
