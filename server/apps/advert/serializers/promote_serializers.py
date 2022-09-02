from rest_framework import serializers

from advert.models import Promote


class PromoteSerializer(serializers.ModelSerializer):
    types_display = serializers.CharField(source="get_types_display")

    class Meta:
        model = Promote
        fields = "__all__"
