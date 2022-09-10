from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

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
    permission_classes = [IsAdminUser]


class SubCategoryViewSet(ModelViewSet):
    serializer_class = SubCategorySerializerAD
    queryset = SubCategory.objects.all()
    permission_classes = [IsAdminUser]


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializerAD
    queryset = Category.objects.all()
    permission_classes = [IsAdminUser]


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializerAD
    queryset = Comment.objects.all()
    permission_classes = [IsAdminUser]


class CityViewSet(ModelViewSet):
    serializer_class = CitySerializerAD
    queryset = City.objects.all()
    permission_classes = [IsAdminUser]


class FavoriteAdvertViewSet(ModelViewSet):
    serializer_class = FavoriteAdvertSerializerAD
    queryset = FavoriteAdvert.objects.all()
    permission_classes = [IsAdminUser]


class AdvertContactViewSet(ModelViewSet):
    serializer_class = AdvertContactSerializerAD
    queryset = AdvertContact.objects.all()
    permission_classes = [IsAdminUser]


class PromoteViewSet(ModelViewSet):
    serializer_class = PromoteSerializerAD
    queryset = Promote.objects.all()
    permission_classes = [IsAdminUser]


class ChatViewSet(ModelViewSet):
    serializer_class = ChatSerializerAD
    queryset = Chat.objects.all()
    permission_classes = [IsAdminUser]


class AdvertImageViewSet(ModelViewSet):
    serializer_class = AdvertImageSerializerAD
    queryset = AdvertImage.objects.all()
    permission_classes = [IsAdminUser]


class AdvertViewSet(ModelViewSet):
    serializer_class = AdvertSerializerAD
    queryset = Advert.objects.all()
    permission_classes = [IsAdminUser]
