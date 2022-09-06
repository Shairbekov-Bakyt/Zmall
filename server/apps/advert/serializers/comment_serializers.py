from rest_framework import serializers

from advert.models import Comment


class FilterCommentListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterCommentListSerializer
        model = Comment
        fields = ("text", "user", "children")
