from rest_framework import serializers

from advert.models import SubCategory, Advert


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['advert_count'] = Advert.objects.filter(sub_category=instance).count()
        return data