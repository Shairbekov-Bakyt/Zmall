from django.http import HttpRequest
# from django_filters.rest_framework import DjangoFilterBackend, FilterSet,
from django_filters import rest_framework as filter
from rest_framework import filters

from rest_framework import status
from rest_framework.filters import OrderingFilter, BaseFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from advert.api import serializers
from advert.models import Advert
from advert.selectors import get_advert


class PriceFilter(filter.FilterSet):
    from_price = filter.RangeFilter()

    class Meta:
        model = Advert
        fields = ('from_price', 'city')


class AdvertViewSet(ModelViewSet):
    queryset = Advert.objects.filter(is_active=True)
    serializer_class = serializers.AdvertCreateSerializer
    filter_backends = [filter.DjangoFilterBackend, OrderingFilter]

    filterset_class = PriceFilter
    ordering_fields = ['created_date', 'to_price']
    ordering = ['created_date']

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.AdvertListSerializer
        return super().get_serializer_class()

    def retrieve(self, request: HttpRequest, pk=None) -> Response:
        advert = get_advert(pk)
        serializer = serializers.AdvertDetailSerializer(advert)
        advert.view += 1
        advert.save()
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        obj = request
