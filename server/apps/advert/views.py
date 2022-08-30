from django.http import HttpRequest

from django_filters import rest_framework as rest_filters
from rest_framework import status, filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from advert.api import serializers
from advert.models import Advert
from advert.selectors import get_advert_by_id
from advert.task import task_send_advert_to_email
from user.models import CustomUser


class PriceFilter(rest_filters.FilterSet):
    from_price = rest_filters.RangeFilter()

    class Meta:
        model = Advert
        fields = ("from_price", "city")


class AdvertViewSet(ModelViewSet):
    queryset = Advert.objects.filter(is_active=True)
    serializer_class = serializers.AdvertCreateSerializer
    filter_backends = [rest_filters.DjangoFilterBackend, filters.OrderingFilter]

    filterset_class = PriceFilter
    ordering_fields = ["created_date", "to_price"]
    ordering = ["created_date"]

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.AdvertListSerializer
        return super().get_serializer_class()

    def retrieve(self, request: HttpRequest, pk=None) -> Response:
        advert = get_advert_by_id(pk)
        serializer = serializers.AdvertDetailSerializer(advert)

        advert.view += 1
        advert.save()

        send_advert_to_email.delay("hello")
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: HttpRequest) -> Response:
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        advert = Advert.objects.get(id=1)
        for user in CustomUser.objects.all():
            task_send_advert_to_email.delay(user.email, advert.id, advert.name)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

