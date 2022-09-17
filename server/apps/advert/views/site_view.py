from rest_framework.viewsets import ModelViewSet

from advert.api.footerlinks_serializers import FooterLinkSerializer
from advert.models import FooterLink


class FooterLinksView(ModelViewSet):
    queryset = FooterLink.objects.all()
    serializer_class = FooterLinkSerializer
