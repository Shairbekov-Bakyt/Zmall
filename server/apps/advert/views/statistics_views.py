from rest_framework.generics import ListAPIView
from rest_framework import filters

from advert.models import AdvertStatistics
from advert.serializers import statistics_serializers as serializers


class StatisticsView(ListAPIView):
    queryset = AdvertStatistics.objects.all()
    serializer_class = serializers.StatisticsSerializer
    filter_backends = [
        filters.OrderingFilter
    ]
    ordering_fields = ["date"]
