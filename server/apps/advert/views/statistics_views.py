import django_filters
from rest_framework.generics import ListAPIView
from rest_framework import filters

from advert.models import AdvertStatistics
from advert.serializers import statistics_serializers as serializers


class AdvertStatisticsFilter(django_filters.FilterSet):
    date = django_filters.DateTimeFromToRangeFilter(field_name="date")


class StatisticsView(ListAPIView):
    queryset = AdvertStatistics.objects.all()
    serializer_class = serializers.StatisticsSerializer
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.OrderingFilter
    ]
    filterset_class = AdvertStatisticsFilter
    ordering_fields = ["date"]
    ordering = ["date"]
