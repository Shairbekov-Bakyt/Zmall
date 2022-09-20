from django.db import transaction

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from advert.api.transaction_serializers import TransactionListSerializer
from advert.models import Transaction


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionListSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
            data = request.data
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)