from rest_framework import serializers


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
        fields = ("phone_number")


class AdvertImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertImage
        fields = ("image",)


class AdvertCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    sub_category = serializers.SlugRelatedField(slug_field='name', queryset=SubCategory.objects.all())
    promote = serializers.SlugRelatedField(slug_field='name', queryset=Promote.objects.all())
    city = serializers.SlugRelatedField(slug_field='name', queryset=City.objects.all())
    advert_image = serializers.ImageField()

    class Meta:
        model = Advert
        fields = (
            "owner",
            "name",
            "category",
            "sub_category",
            "from_price",
            "to_price",
            "description",
            "city",
            "email",
            "phone_number",
            "wa_number",
            "promote",
            "advert_image",
        )


class AdvertListSerializer(serializers.ModelSerializer):
    promote = serializers.SlugRelatedField(slug_field="types", read_only=True)
    advert_image = AdvertImageSerializer(many=True)

    class Meta:
        model = Advert
        fields = ("id", "name", "from_price", "sub_category", "promote", "advert_image")


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
