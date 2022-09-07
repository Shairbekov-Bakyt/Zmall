from rest_framework.viewsets import ModelViewSet

from custom_admin.serializers import *
from advert.models import (
    Advert,
    AdvertImage,
    AdvertContact,
    FavoriteAdvert,
    City,
    Comment,
    Category,
    SubCategory,
)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializerAD
    queryset = CustomUser.objects.all()


class SubCategoryViewSet(ModelViewSet):
    serializer_class = SubCategorySerializerAD
    queryset = SubCategory.objects.all()


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializerAD
    queryset = Category.objects.all()


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializerAD
    queryset = Comment.objects.all()


class CityViewSet(ModelViewSet):
    serializer_class = CitySerializerAD
    queryset = City.objects.all()


class FavoriteAdvertViewSet(ModelViewSet):
    serializer_class = FavoriteAdvertSerializerAD
    queryset = FavoriteAdvert.objects.all()


class AdvertContactViewSet(ModelViewSet):
    serializer_class = AdvertContactSerializerAD
    queryset = AdvertContact.objects.all()


class PromoteViewSet(ModelViewSet):
    serializer_class = PromoteSerializerAD
    queryset = Promote.objects.all()


class ChatViewSet(ModelViewSet):
    serializer_class = ChatSerializerAD
    queryset = Chat.objects.all()


class AdvertImageViewSet(ModelViewSet):
    serializer_class = AdvertImageSerializerAD
    queryset = AdvertImage.objects.all()


class AdvertViewSet(ModelViewSet):
    serializer_class = AdvertSerializerAD
    queryset = Advert.objects.all()