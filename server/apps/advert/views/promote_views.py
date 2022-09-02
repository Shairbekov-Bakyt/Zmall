from rest_framework.viewsets import ModelViewSet

from advert.serializers import promote_serializers as serializers
from advert.models import Promote


class PromoteViewSet(ModelViewSet):
    queryset = Promote.objects.all()
    serializer_class = serializers.PromoteSerializer
    http_method_names = ["get"]
