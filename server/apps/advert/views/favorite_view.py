from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import UpdateAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from advert.models import FavoriteAdvert, Advert
from advert.serializers.favorite_serializer import FavoriteSerializer
from advert.utils import get_request_data_for_favorite


class FavoriteUpdateDelete(UpdateAPIView):
    queryset = FavoriteAdvert.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def put(self,request, advert_id, delete, *args, **kwargs):
        try:
            Advert.objects.get_or_create(pk=advert_id)
        except:
            return Response({"advert" : f"with id {advert_id} does not exists"}, status=status.HTTP_404_NOT_FOUND)

        advert = FavoriteAdvert.objects.get_or_create(user_id=request.user)[0]
        if delete:
            advert.adverts.add(advert_id)
        else:
            advert.adverts.remove(advert_id)

        advert.save()
        serializer = self.get_serializer(advert)
        return Response(serializer.data, status=status.HTTP_200_OK)





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
