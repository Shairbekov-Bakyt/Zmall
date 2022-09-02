from rest_framework.generics import ListAPIView

from advert.serializers.category_serializers import CategorySerializer
from advert.models import Category


class CategoryView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer