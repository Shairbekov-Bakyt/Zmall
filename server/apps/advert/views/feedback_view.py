from rest_framework.viewsets import ModelViewSet

from advert.models import Feedback
from advert.serializers.feedback_serializer import FeedbackSerializer


class FeedbackView(ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer