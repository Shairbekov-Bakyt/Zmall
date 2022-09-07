from rest_framework.serializers import ModelSerializer

from user.models import CustomUser
from chat.models import Chat
from advert.models import (
    Advert,
    AdvertImage,
    AdvertContact,
    FavoriteAdvert,
    City,
    Comment,
    Category,
    Promote,
    SubCategory,
)


class UserSerializerAD(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class CommentSerializerAD(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CitySerializerAD(ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class FavoriteAdvertSerializerAD(ModelSerializer):
    class Meta:
        model = FavoriteAdvert
        fields = '__all__'


class AdvertSerializerAD(ModelSerializer):
    class Meta:
        model = Advert
        fields = '__all__'


class AdvertImageSerializerAD(ModelSerializer):
    class Meta:
        model = AdvertImage
        fields = '__all__'


class AdvertContactSerializerAD(ModelSerializer):
    class Meta:
        model = AdvertContact
        fields = '__all__'


class CategorySerializerAD(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializerAD(ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class PromoteSerializerAD(ModelSerializer):
    class Meta:
        model = Promote
        fields = '__all__'


class ChatSerializerAD(ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'