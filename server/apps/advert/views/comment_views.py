from rest_framework.viewsets import ModelViewSet

import advert.serializers.comment_serializers as serializers
from advert.models import Comment


class CommentView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentCreateSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.CommentSerializer
        return super().get_serializer_class()

