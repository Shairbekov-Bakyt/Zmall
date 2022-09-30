from rest_framework import serializers

from advert.models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["advert_count"] = Advert.objects.filter(category=instance, status='act').count()
        return data


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteAdvert
        fields = ("adverts", "user_id")
        write_only_fields = "user_id"


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"


class FooterLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterLink
        fields = "__all__"

    def to_representation(self, instance):
        data = {"links": super().to_representation(instance), "text": "@ 2022 все права защищены"}
        return data


class HelpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Help
        fields = "__all__"


class HelpCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpCategory
        fields = "__all__"


class PromoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promote
        fields = "__all__"


class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertStatistics
        fields = "__all__"


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["advert_count"] = Advert.objects.filter(sub_category=instance, status='act').count()
        return data


class TransactionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class FeedbackMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackMessage
        fields = ("text",)


class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = ("title", "text")
