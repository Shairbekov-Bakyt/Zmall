from rest_framework import serializers

from advert.models import Category, Advert


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['advert_count'] = Advert.objects.filter(category=instance).count()
        return data