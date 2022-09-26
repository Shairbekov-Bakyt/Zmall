from django.db import transaction

import requests
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from decouple import config

from advert.api.transaction_serializers import TransactionListSerializer
from advert.models import Transaction
from advert.utils import generate_sig, get_url_from_content


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionListSerializer
    permission_classes = [IsAuthenticated, ]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        data.owner = request.user
        data.save()
        method = 'init_payment.php'
        params = generate_sig(data, 'init_payment.php')
        response = requests.post(url=config('PAYBOX_BASE_URL')+method, params=params)
        url = get_url_from_content(response.content)
        return Response({**serializer.data, 'redirect_url': url})