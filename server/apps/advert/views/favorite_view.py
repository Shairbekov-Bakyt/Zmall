from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from advert.models import FavoriteAdvert
from advert.serializers.favorite_serializer import FavoriteSerializer


class FavoriteAdvertView(ModelViewSet):
    queryset = FavoriteAdvert.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        data = request.data
        data['user_id'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def list(self, request):
        query = get_object_or_404(FavoriteAdvert, user_id=request.user.id)
        serializer = self.get_serializer(query)
        return Response(serializer.data)

    
