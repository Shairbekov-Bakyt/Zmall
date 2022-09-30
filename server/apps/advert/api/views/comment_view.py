from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from advert.models import Comment
from advert.selectors import recursive_sql_query
import advert.api.serializers.comment_serializers as serializers


class CommentView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentCreateSerializer

    def list(self, request, *args, **kwargs):
        comments = recursive_sql_query()
        serializer = serializers.CommentSerializer(comments, many=True)
        return Response(serializer.data)
