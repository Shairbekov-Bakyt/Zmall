import django_filters
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from phonenumber_field.validators import validate_international_phonenumber
from rest_framework.response import Response

from advert.api.advert_serializers import *
from custom_admin.serializers import UserSerializerAD
from advert.api.pagination import AdvertPagination
from advert.models import (
    Advert,
    AdvertImage,
    AdvertContact,
)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializerAD
    queryset = CustomUser.objects.all()
    permission_classes = [IsAdminUser]
    http_method_names = ["get", "put", "delete"]


class AdvertFilter(django_filters.FilterSet):
    advert_reports = django_filters.BooleanFilter(
        lookup_expr="isnull", field_name="advert_reports"
    )



class AdvertViewSet(ModelViewSet):
    queryset = Advert.objects.select_related('category', 'sub_category').all()
    serializer_class = AdvertCreateSerializer
    filterset_class = AdvertFilter
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    pagination_class = AdvertPagination
    permission_classes = [IsAdminUser]
    http_method_names = ["get", 'put', 'delete']

    def create(self, request, *args, **kwargs):
        imgs = request.FILES.getlist("image")
        if len(imgs) > 8:
            raise serializers.ValidationError("Максимальное кол-во изображений: 8")

        contacts = request.data.getlist("advert_contact")

        if len(imgs) > 8:
            raise serializers.ValidationError("Максимальное кол-во контактов: 8")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        advert = serializer.save()

        img_objects = []
        for img in imgs:
            img_objects.append(AdvertImage(advert=advert, image=img))

        AdvertImage.objects.bulk_create(img_objects)

        ad_contacts = []
        for contact in contacts[0].split(','):
            validate_international_phonenumber(contact)
            ad_contacts.append(AdvertContact(advert=advert, phone_number=contact))

        AdvertContact.objects.bulk_create(ad_contacts)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.action == "list":
            return AdvertListSerializer
        if self.action == 'retrieve':
            return AdvertDetailSerializer
        return super().get_serializer_class()
