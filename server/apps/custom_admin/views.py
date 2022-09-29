import django_filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

from user.models import CustomUser
from user.api.serializers import RegisterSerializer
from advert.views.advert_view import AdvertViewSet
from custom_admin.serializers import UserSerializerAD, AdReportSerializer
from advert.api.pagination import AdvertPagination
from advert.models import Advert, AdvertReport


class UserViewSet(ModelViewSet):
    serializer_class = RegisterSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return UserSerializerAD
        return super().get_serializer_class()


class AdvertFilter(django_filters.FilterSet):
    advert_reports = django_filters.BooleanFilter(
        lookup_expr="isnull", field_name="advert_reports"
    )


#
class AdReportView(ModelViewSet):
    queryset = AdvertReport.objects.all()
    serializer_class = AdReportSerializer
    http_method_names = ["get"]
    permission_classes = [IsAdminUser]


class AdvertView(AdvertViewSet):
    queryset = Advert.objects.select_related("category", "sub_category").all()
    filterset_class = AdvertFilter
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    pagination_class = AdvertPagination
    http_method_names = ["get", "put", "delete"]
    permission_classes = [IsAdminUser]



