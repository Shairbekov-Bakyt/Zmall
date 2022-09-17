from rest_framework import serializers

from advert.models import AdvertStatistics


class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertStatistics
        fields = "__all__"
