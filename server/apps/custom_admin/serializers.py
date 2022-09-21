from rest_framework import serializers

from user.models import CustomUser
from advert.models import (
    Advert,
    City,
    AdvertImage,
    AdvertContact,
    Feedback,
    Category,
    SubCategory,
    Promote,
    AdvertReport,
)


class UserSerializerAD(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "first_name", "last_name", "phone_number", "email")


class CustomerFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ("id", "name", "email", "feedback_title", "message")


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class AdvertContactSerailzer(serializers.ModelSerializer):
    class Meta:
        model = AdvertContact
        fields = ("phone_number",)


class AdvertImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertImage
        fields = ["image"]


class AdReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertReport
        fields = "__all__"


class AdminAdvertSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        slug_field="id", queryset=CustomUser.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="id", queryset=Category.objects.all()
    )
    sub_category = serializers.SlugRelatedField(
        slug_field="id", queryset=SubCategory.objects.all()
    )
    promote = serializers.SlugRelatedField(
        slug_field="types", queryset=Promote.objects.all(), allow_null=True
    )
    city = serializers.SlugRelatedField(slug_field="id", queryset=City.objects.all())

    class Meta:
        model = Advert
        exclude = ("created_date", "status")
