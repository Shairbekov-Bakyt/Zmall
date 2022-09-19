import django_filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

from advert.api.advert_serializers import *
from advert.views.advert_view import AdvertViewSet
from custom_admin.serializers import UserSerializerAD
from advert.api.pagination import AdvertPagination
from advert.models import Advert


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializerAD
    queryset = CustomUser.objects.all()
    permission_classes = [IsAdminUser]
    http_method_names = ["get", "put", "delete"]


class AdvertFilter(django_filters.FilterSet):
    advert_reports = django_filters.BooleanFilter(
        lookup_expr="isnull", field_name="advert_reports"
    )


class AdvertView(AdvertViewSet):
    queryset = Advert.objects.select_related("category", "sub_category").all()
    serializer_class = AdvertCreateSerializer
    filterset_class = AdvertFilter
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    pagination_class = AdvertPagination
    http_method_names = ["get", "put", "delete"]
    permission_classes = [IsAdminUser]