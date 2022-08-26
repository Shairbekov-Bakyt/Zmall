from django.http import HttpRequest
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
# from django_filters import rest_framework as filter
from rest_framework import filters

from rest_framework.filters import OrderingFilter, BaseFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from advert.api import serializers
from advert.models import Advert
from advert.selectors import get_advert


class PriceFilter(FilterSet):
    # from_price = filter.RangeFilter()

    class Meta:
        model = Advert
        fields = ('from_price', 'city')


class AdvertViewSet(ModelViewSet):
    queryset = Advert.objects.all()
    serializer_class = serializers.AdvertCreateSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    filterset_fields = ['city']
    # filterset_fields = ['city']
    # filterset_class = PriceFilter
    ordering_fields = ['created_date', 'to_price']
    ordering = ['created_date']

    def list(self, request: HttpRequest) -> Response:
        adverts = Advert.objects.filter(is_active=True).order_by('-created_date')
        serializer = serializers.AdvertListSerializer(adverts, many=True)
        return Response(serializer.data)

    def retrieve(self, request: HttpRequest, pk=None) -> Response:
        advert = get_advert(pk)
        serializer = serializers.AdvertDetailSerializer(advert)
        advert.view += 1
        advert.save()
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        ad_data = request.data

        # serializer = serializers.AdvertCreateSerializer(data=ad_data)
        # if serializer.is_valid():
        #     serializer.save()
        super().create(request)
        return Response({'success': f'Advertisement {ad_data["name"]} created successfully!'})
