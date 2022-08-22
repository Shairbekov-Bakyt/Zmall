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


class PromoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promote
        fields = ("id", "icon", "types")


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "name")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "advert_count", "icon")


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ("id", "category", "name", "advert_count")


class AdvertContactSerailzer(serializers.ModelSerializer):
    class Meta:
        model = AdvertContact
        fields = ("id", "phone_number")


class AdvertImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertImage
        fields = ("id", "image")


class AdvertCreateSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    sub_category = SubCategorySerializer()
    promote = PromoteSerializer()
    city = CitySerializer()

    class Meta:
        model = Advert
        fields = (
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
            "created_date",
            "image_count",
            "view",
            "is_active",
            "is_verified",
        )


class AdvertListSerializer(serializers.ModelSerializer):
    promote = PromoteSerializer()

    class Meta:
        model = Advert
        fields = ("name", "from_price", "sub_category", "promote")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        advert = AdvertImage.objects.filter(advert=instance).first()
        representation['image'] = advert.image.url

        return representation


class AdvertDetailSerializer(serializers.ModelSerializer):
    promote = PromoteSerializer()
    advert_contact = AdvertContactSerailzer(many=True)
    city = CitySerializer()
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

