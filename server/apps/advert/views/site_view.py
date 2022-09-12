from rest_framework.viewsets import ModelViewSet

from advert.serializers.footerlinks_serializer import FooterLinkSerializer
from advert.models import FooterLink


class FooterLinksView(ModelViewSet):
    queryset = FooterLink.objects.all()
    serializer_class = FooterLinkSerializer
