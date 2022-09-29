import json
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from user.models import CustomUser as User
from advert.utils import connect_to_redis
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
    views = serializers.SerializerMethodField(source='get_views', read_only=True)

    def get_views(self, instance):
        view = connect_to_redis()
        redis_views = view.get(instance.id)
        ad_views = 0

        if redis_views is not None:
            redis_views = json.loads(redis_views.decode("utf-8"))
            ad_views = redis_views['views_counter']

        return ad_views

    class Meta:
        model = Advert
        exclude = ("created_date", "status")


class UserPatchSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=False,
        validators=[
            UniqueValidator(queryset=User.objects.all(), message="email уже занят")
        ],
    )

    password = serializers.CharField(
        write_only=True, required=False, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = "__all__"

        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "phone_number": {"required": True},
        }

