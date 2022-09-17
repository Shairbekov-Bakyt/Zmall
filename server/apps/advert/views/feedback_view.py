from rest_framework.viewsets import ModelViewSet

from advert.models import Feedback
from advert.api.feedback_serializers import FeedbackSerializer


class FeedbackView(ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
