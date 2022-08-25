from django.http import HttpRequest
from django_filters.rest_framework import DjangoFilterBackend, NumericRangeFilter

from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from advert.api import serializers
from advert.models import Advert

from advert.selectors import get_advert


class AdvertViewSet(ModelViewSet):
    queryset = Advert.objects.all()
    serializer_class = serializers.AdvertCreateSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    filterset_fields = ['city', 'from_price', 'to_price', 'is_active']
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
        request.data['owner'] = request.user
        super().create(request)
