from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from advert.models import FavoriteAdvert
from advert.serializers.favorite_serializer import FavoriteSerializer
from advert.utils import get_request_data_for_favorite


class FavoriteAdvertView(ModelViewSet):
    queryset = FavoriteAdvert.objects.select_related('adverts', 'user_id').all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):

        data = get_request_data_for_favorite(request)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def list(self, request):
        try:
            query = FavoriteAdvert.objects.prefetch_related('adverts', 'user_id').get(user_id=request.user.id)
        except:
            return Response({"favorite": "empty"})

        serializer = self.get_serializer(query)
        return Response(serializer.data)

    
