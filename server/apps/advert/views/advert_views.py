from django.http import HttpRequest

from django_filters import rest_framework as rest_filters
from rest_framework import status, filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from advert.serializers import advert_serializers as serializers
from advert.models import Advert, AdvertImage, AdvertView

from advert.serializers import permissions


class PriceFilter(rest_filters.FilterSet):
    from_price = rest_filters.RangeFilter()

    class Meta:
        model = Advert
        fields = ("start_price", "city")


class AdvertViewSet(ModelViewSet):
    queryset = Advert.objects.all()
    serializer_class = serializers.AdvertCreateSerializer
    filter_backends = [rest_filters.DjangoFilterBackend, filters.OrderingFilter]
    permission_classes = [permissions.IsOwnerOrReadOnly]
    filterset_class = PriceFilter
    ordering_fields = ["created_date", "end_price"]
    ordering = ["created_date"]

    def retrieve(self, request: HttpRequest, pk) -> Response:
        advert = self.get_object()
        serializer = serializers.AdvertDetailSerializer(advert)

        user = request.user
        advert_view, _ = AdvertView.objects.get_or_create(advert=advert)

        if user not in advert_view.users.all():
            advert_view.users.add(user)
            advert_view.view += 1
            advert_view.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        imgs = request.FILES.getlist('image')
        if len(imgs) > 8:
            raise serializers.ValidationError("Максимальное кол-во изображений: 8")

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            advert = serializer.save()

        img_objects = []
        for img in imgs:
            img_objects.append(AdvertImage(advert_id=advert, image=img))

        AdvertImage.objects.bulk_create(img_objects)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.AdvertListSerializer
        return super().get_serializer_class()



