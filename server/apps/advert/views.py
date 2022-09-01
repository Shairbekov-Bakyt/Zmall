from django.http import HttpRequest

from django_filters import rest_framework as rest_filters
from rest_framework import status, filters
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response

from advert.api import serializers
from advert.models import Advert, AdvertImage
from advert.selectors import get_advert_by_id
from advert.task import task_send_advert_to_email
from advert.utils import modify_input_for_multiple_files

from user.models import CustomUser


class ImageView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        all_images = AdvertImage.objects.all()
        serializer = serializers.AdvertImageSerializer(all_images, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        property_id = request.data['advert_id']
        images = dict((request.data).lists())['image']
        flag = 1
        result = []
        for img_name in images:
            modified_data = modify_input_for_multiple_files(property_id,
                                                            img_name)
            file_serializer = serializers.AdvertImageSerializer(data=modified_data)
            if file_serializer.is_valid():
                file_serializer.save()
                result.append(file_serializer.data)
            else:
                flag = 0

        if flag != 1:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        return Response(result, status=status.HTTP_201_CREATED)



class PriceFilter(rest_filters.FilterSet):
    from_price = rest_filters.RangeFilter()

    class Meta:
        model = Advert
        fields = ("from_price", "city")


class AdvertViewSet(ModelViewSet):
    queryset = Advert.objects.filter(is_active=True)
    serializer_class = serializers.AdvertCreateSerializer
    filter_backends = [rest_filters.DjangoFilterBackend, filters.OrderingFilter]
    permission_classes = []
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

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: HttpRequest) -> Response:
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        advert = get_advert_by_id(1)
        for user in CustomUser.objects.all():
            task_send_advert_to_email.delay(user.email, advert.id, advert.name)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
