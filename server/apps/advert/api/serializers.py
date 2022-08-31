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
)


class AdvertContactSerailzer(serializers.ModelSerializer):
    class Meta:
        model = AdvertContact
        fields = ("phone_number",)


class AdvertImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertImage
        fields = ["image"]


class AdvertCreateSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='email', queryset=CustomUser.objects.all())
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    sub_category = serializers.SlugRelatedField(slug_field='name', queryset=SubCategory.objects.all())
    promote = serializers.SlugRelatedField(slug_field='name', queryset=Promote.objects.all())
    city = serializers.SlugRelatedField(slug_field='name', queryset=City.objects.all())
    advert_image = AdvertImageSerializer(write_only=True)
    # advert_image = AdvertImageSerializer(write_only=True, required=False)
    # advert_contact = AdvertContactSerailzer(write_only=True, required=False)

    def create(self, validated_data):
        print(validated_data)
        advert_image = validated_data.pop('advert_image')
        advert = Advert.objects.create(**validated_data)
        AdvertImage.objects.create(advert=advert, **advert_image)
        return advert

    class Meta:
        model = Advert

        exclude = (
            "created_date",
            "image_count",
            "view",
            "is_active",
            "is_verified",
            )


class AdvertListSerializer(serializers.ModelSerializer):
    promote = serializers.SlugRelatedField(slug_field="types", read_only=True)
    advert_image = AdvertImageSerializer(many=True)

    class Meta:
        model = Advert
        fields = (
            "id",
            "name",
            "from_price",
            "sub_category",
            "promote",
            "advert_image",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        advert = AdvertImage.objects.filter(advert=instance).first()
        if advert:
            representation["image"] = advert.image.url

        return representation
        


class AdvertDetailSerializer(serializers.ModelSerializer):
    promote = serializers.SlugRelatedField(slug_field="types", read_only=True)
    advert_contact = AdvertContactSerailzer(many=True)
    city = serializers.SlugRelatedField(slug_field="name", read_only=True)
    advert_image = AdvertImageSerializer(many=True)

    class Meta:
        model = Advert
        fields = [
            "id",
            "name",
            "owner",
            "from_price",
            "description",
            "wa_number",
            "phone_number",
            "view",
            "created_date",
            "city",
            "promote",
            "advert_image",
            "advert_contact",
        ]
