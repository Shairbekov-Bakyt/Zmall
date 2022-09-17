from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from advert.models import Comment
from advert.selectors import recrursive_sql_query
import advert.api.comment_serializers as serializers


class CommentView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentCreateSerializer

    def list(self, request, *args, **kwargs):
        comments = recrursive_sql_query()
        serializer = serializers.CommentSerializer(comments, many=True)
        return Response(serializer.data)
