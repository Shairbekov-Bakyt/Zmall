from rest_framework import serializers

from user.models import CustomUser
from apps.advert.utils import connect_to_redis
from advert.serializers.promote_serializers import PromoteSerializer
from advert.models import (
    Advert,
    AdvertContact,
    AdvertImage,
    Category,
    SubCategory,
    City,
    AdvertView,
    AdvertReport,
)


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class AdvertContactSerailzer(serializers.ModelSerializer):
    class Meta:
        model = AdvertContact
        fields = ("phone_number",)


class AdvertViewSerailzer(serializers.ModelSerializer):
    class Meta:
        model = AdvertView
        fields = ("view", "users")


class AdvertImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertImage
        fields = ["image"]


class AdvertCreateSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        slug_field="email", queryset=CustomUser.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="name", queryset=Category.objects.all()
    )
    sub_category = serializers.SlugRelatedField(
        slug_field="name", queryset=SubCategory.objects.all()
    )
    promote = PromoteSerializer(many=True, required=False)
    city = serializers.SlugRelatedField(slug_field="name", queryset=City.objects.all())

    class Meta:
        model = Advert

        exclude = ("created_date", "status")


class AdvertListSerializer(serializers.ModelSerializer):
    promote = PromoteSerializer(many=True)
    sub_category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    advert_contact = AdvertContactSerailzer(many=True)
    advert_image = AdvertImageSerializer(many=True)
    advert_image_count = serializers.IntegerField(
        source="advert_image.count", read_only=True
    )
    city = serializers.SlugRelatedField(slug_field="name", queryset=City.objects.all())

    class Meta:
        model = Advert
        fields = (
            "id",
            "name",
            "sub_category",
            "start_price",
            "end_price",
            "promote",
            "advert_image",
            "advert_image_count",
            "advert_contact",
            "views",
            "city",
            "created_date",
            "description"
        )


class AdvertDetailSerializer(serializers.ModelSerializer):
    promote = PromoteSerializer(many=True, read_only=True)
    advert_contact = AdvertContactSerailzer(many=True)
    city = serializers.SlugRelatedField(slug_field="name", read_only=True)
    advert_image = AdvertImageSerializer(many=True)
    views = serializers.SerializerMethodField(source='get_views', read_only=True)

    class Meta:
        model = Advert
        exclude = ("email",)

    def get_views(self, instance):
        view = connect_to_redis()
        ad_views = view.get(f'{instance.id}_view')

        return ad_views


class AdvertReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertReport
        fields = '__all__'
