import django_filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from advert.models import Help, HelpCategory
from advert.serializers.help_serializer import HelpSerializer, HelpCategorySerializer


class FAQListView(ListAPIView):
    queryset = Help.objects.select_related('help_category').order_by('-view')[:10]
    serializer_class = HelpSerializer


class HelpViewSet(ModelViewSet):
    queryset = Help.objects.select_related('help_category').all()
    serializer_class = HelpSerializer
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
    ]

    filterset_fields = ['help_category']

    def retrieve(self, request, pk, *args, **kwargs):
        obj = Help.objects.get(pk=pk)
        obj.view += 1
        obj.save()
        serialzier = self.get_serializer(obj)
        return Response(serialzier.data)


class HelpCategoryViewSet(ModelViewSet):
    queryset = HelpCategory.objects.all()
    serializer_class = HelpCategorySerializer
