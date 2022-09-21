import django_filters
from rest_framework import status, filters
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from phonenumber_field.validators import validate_international_phonenumber

from advert.api import permissions
from advert.selectors import advert_with_select_related_filter
from advert.api import advert_serializers as serializers
from advert.api.pagination import AdvertPagination
from config.middleware import get_client_ip
from advert.services import (
    set_advert_contacts_count,
    create_ad_imgs,
    create_ad_contacts,
    delete_ad_imgs,
    delete_ad_contacts
)
from advert.models import (
    Advert,
    AdvertImage,
    City,
    AdvertContact,
    AdvertReport,
    FeedbackMessage,
    PrivacyPolicy,
)


class AdvertFilter(django_filters.FilterSet):
    start_price = django_filters.RangeFilter(field_name="start_price")

    city = django_filters.ModelMultipleChoiceFilter(
        field_name="city", queryset=City.objects.all()
    )
    image = django_filters.BooleanFilter(
        lookup_expr="isnull", field_name="advert_image", distinct=True
    )

    class Meta:
        model = Advert
        fields = ["category", "sub_category"]


class CityListView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = serializers.CitySerializer


class AdvertViewSet(ModelViewSet):
    queryset = advert_with_select_related_filter("act")
    serializer_class = serializers.AdvertCreateSerializer
    pagination_class = AdvertPagination
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    permission_classes = [permissions.IsOwnerOrReadOnly]
    filterset_class = AdvertFilter
    ordering_fields = ["created_date", "start_price"]
    ordering = ["created_date"]
    search_fields = ["name"]

    def create(self, request, *args, **kwargs):
        imgs = request.FILES.getlist("image")
        contacts = request.data.getlist("advert_contact")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        advert = serializer.save()

        img_objects = []
        for img in imgs:
            img_objects.append(AdvertImage(advert=advert, image=img))

        AdvertImage.objects.bulk_create(img_objects)

        ad_contacts = []
        for contact in contacts[0].split(","):
            validate_international_phonenumber(contact)
            ad_contacts.append(AdvertContact(advert=advert, phone_number=contact))

        AdvertContact.objects.bulk_create(ad_contacts)
        create_ad_imgs(advert, imgs)
        create_ad_contacts(advert, contacts)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        imgs = request.FILES.getlist("image")
        contacts = request.data.getlist("advert_contact")

        delete_ad_imgs(instance.id)
        delete_ad_contacts(instance.id)

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        create_ad_imgs(instance, imgs)
        create_ad_contacts(instance, contacts)

        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.AdvertListSerializer
        if self.action == "retrieve":
            return serializers.AdvertDetailSerializer
        return super().get_serializer_class()


class PremiumAdvertView(AdvertViewSet):
    queryset = Advert.objects.filter(status="act", promote__isnull=False)
    serializer_class = serializers.AdvertListSerializer


class ContactView(CreateAPIView):
    queryset = AdvertContact.objects.select_related("category", "sub_category").all()

    def post(self, request, advert_id: int, *args, **kwargs):
        user = request.user
        ip = get_client_ip(request)
        set_advert_contacts_count(advert_id, str(user), ip)
        return Response(
            {"advert_contact": "counter updated"}, status=status.HTTP_200_OK
        )


class AdvertReportView(CreateAPIView):
    queryset = AdvertReport.objects.all()
    serializer_class = serializers.AdvertReportSerializer


class UserAdvertFilter(django_filters.FilterSet):
    class Meta:
        model = Advert
        fields = ["status"]


class UserAdvertView(ListAPIView):
    serializer_class = serializers.UserAdvertDetailSerializer
    queryset = Advert.objects.all()
    filterset_class = UserAdvertFilter
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    def get_queryset(self):
        user = self.request.user
        return Advert.objects.filter(owner__email=user)


class UserAdvertUpdateView(UpdateAPIView):
    queryset = Advert.objects.all()
    serializer_class = serializers.AdvertCreateSerializer
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "advert updated successfully"})

        else:
            return Response(
                {"message": "failed", "details": serializer.errors},
                status=status.HTTP_304_NOT_MODIFIED,
            )


class FeedbackMessageView(ListAPIView):
    serializer_class = serializers.FeedbackMessageSerializer
    queryset = FeedbackMessage.objects.all()


class PrivacyPolicyView(ListAPIView):
    serializer_class = serializers.PrivacyPolicySerializer
    queryset = PrivacyPolicy.objects.all()
