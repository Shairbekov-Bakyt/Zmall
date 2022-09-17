from rest_framework.generics import ListAPIView

from advert.api.sub_category_serializers import SubCategorySerializer
from advert.models import SubCategory


class SubCategoryView(ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
