import django_filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

from advert.models import Help, HelpCategory
from advert.serializers.help_serializer import HelpSerializer, HelpCategorySerializer


class FAQListView(ListAPIView):
    queryset = Help.objects.order_by('-view')[:10]
    serializer_class = HelpSerializer


class HelpViewSet(ModelViewSet):
    queryset = Help.objects.all()
    serializer_class = HelpSerializer
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
    ]

    filterset_fields = ['help_category']

    def retrieve(self, request, pk, *args, **kwargs):
        obj = Help.objects.get(pk=pk)
        obj.view += 1
        obj.save()
        super().retrieve(self, request, pk, *args, **kwargs)


class HelpCategoryViewSet(ModelViewSet):
    queryset = HelpCategory.objects.all()
    serializer_class = HelpCategorySerializer