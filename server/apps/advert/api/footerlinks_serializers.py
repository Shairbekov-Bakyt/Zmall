from rest_framework.serializers import ModelSerializer
from advert.models import FooterLink


class FooterLinkSerializer(ModelSerializer):
    class Meta:
        model = FooterLink
        fields = "__all__"

    def to_representation(self, instance):
        data = {}
        data["links"] = super().to_representation(instance)
        data["text"] = "@ 2022 все права защищены"
        return data
