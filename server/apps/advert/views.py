from django.http import HttpRequest

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from advert.api import serializers
from advert.models import Advert

from advert.selectors import get_advert


class AdvertViewSet(ModelViewSet):
    queryset = Advert.objects.all()
    serializer_class = serializers.AdvertCreateSerializer

    def list(self, request: HttpRequest) -> Response:
        adverts = Advert.objects.filter(is_active=True)
        serializer = serializers.AdvertListSerializer(adverts, many=True)
        return Response(serializer.data)

    def retrieve(self, request: HttpRequest, pk=None) -> Response:
        advert = get_advert(pk)
        serializer = serializers.AdvertDetailSerializer(advert)
        advert.view += 1
        advert.save()
        return Response(serializer.data)
