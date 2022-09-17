from rest_framework.serializers import ModelSerializer

from advert.models import FavoriteAdvert


class FavoriteSerializer(ModelSerializer):
    class Meta:
        model = FavoriteAdvert
        fields = ("adverts", "user_id")
        write_only_fields = "user_id"
