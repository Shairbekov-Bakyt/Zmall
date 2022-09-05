from rest_framework import serializers

from user.models import CustomUser
from advert.models import (
    Advert,
    AdvertContact,
    AdvertImage,
    Category,
    SubCategory,
    City,
    Promote,
    AdvertView
)


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


class PromoteSerailzer(serializers.ModelSerializer):
    types_display = serializers.CharField(source="get_types_display")

    class Meta:
        model = Promote
        fields = ("icon", "types_display")


class AdvertCreateSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='email', queryset=CustomUser.objects.all())
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    sub_category = serializers.SlugRelatedField(slug_field='name', queryset=SubCategory.objects.all())
    promote = serializers.SlugRelatedField(slug_field='name', queryset=Promote.objects.all())
    city = serializers.SlugRelatedField(slug_field='name', queryset=City.objects.all())

    class Meta:
        model = Advert

        exclude = (
            "created_date",
            "status"
            )


class AdvertListSerializer(serializers.ModelSerializer):
    promote = PromoteSerailzer()
    sub_category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    advert_contact = AdvertContactSerailzer(many=True)
    advert_image = AdvertImageSerializer(many=True)
    advert_image_count = serializers.IntegerField(
        source='advert_image.count',
        read_only=True
    )

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
        )
        

class AdvertDetailSerializer(serializers.ModelSerializer):
    promote = serializers.SlugRelatedField(slug_field="types", read_only=True)
    advert_contact = AdvertContactSerailzer(many=True)
    city = serializers.SlugRelatedField(slug_field="name", read_only=True)
    advert_image = AdvertImageSerializer(many=True)
    advert_view = AdvertViewSerailzer()

    class Meta:
        model = Advert
        exclude = (
            "email",
        )



