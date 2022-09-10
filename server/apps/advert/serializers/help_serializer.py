from rest_framework.serializers import ModelSerializer

from advert.models import HelpCategory, Help


class HelpSerializer(ModelSerializer):
    class Meta:
        model = Help
        fields = '__all__'


class HelpCategorySerializer(ModelSerializer):
    class Meta:
        model = HelpCategory
        fields = '__all__'