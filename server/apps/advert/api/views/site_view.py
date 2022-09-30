import django_filters
from django.db import transaction
from rest_framework import status, filters
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from advert.api.serializers import site_serializers as serializers
from advert.models import *
from advert.utils import get_request_data_for_favorite, generate_sig, get_payment_details


class FooterLinkView(ModelViewSet):
    queryset = FooterLink.objects.all()
    serializer_class = serializers.FooterLinkSerializer


class FeedbackMessageView(ListAPIView):
    serializer_class = serializers.FeedbackMessageSerializer
    queryset = FeedbackMessage.objects.all()


class PrivacyPolicyView(ListAPIView):
    serializer_class = serializers.PrivacyPolicySerializer
    queryset = PrivacyPolicy.objects.all()


class CategoryView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class FavoriteUpdateDelete(UpdateAPIView):
    queryset = FavoriteAdvert.objects.all()
    serializer_class = serializers.FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, advert_id, delete, *args, **kwargs):
        try:
            Advert.objects.get_or_create(pk=advert_id)
        except Exception as _:
            return Response(
                {"advert": f"with id {advert_id} does not exists"},
                status=status.HTTP_404_NOT_FOUND,
            )

        advert = FavoriteAdvert.objects.get_or_create(user_id=request.user)[0]
        if delete:
            advert.adverts.add(advert_id)
        else:
            advert.adverts.remove(advert_id)

        advert.save()
        serializer = self.get_serializer(advert)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FavoriteAdvertView(ModelViewSet):
    queryset = FavoriteAdvert.objects.select_related("adverts", "user_id").all()
    serializer_class = serializers.FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):

        data = get_request_data_for_favorite(request)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def list(self, request):
        try:
            query = FavoriteAdvert.objects.prefetch_related("adverts", "user_id").get(
                user_id=request.user.id
            )
        except Exception as _:
            return Response({"favorite": "empty"})

        serializer = self.get_serializer(query)
        return Response(serializer.data)


class FeedbackView(ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = serializers.FeedbackSerializer


class FAQListView(ListAPIView):
    queryset = Help.objects.select_related("help_category").order_by("-view")[:10]
    serializer_class = serializers.HelpSerializer


class HelpViewSet(ModelViewSet):
    queryset = Help.objects.select_related("help_category").all()
    serializer_class = serializers.HelpSerializer
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
    ]

    filterset_fields = ["help_category"]

    def retrieve(self, request, pk, *args, **kwargs):
        obj = Help.objects.get(pk=pk)
        obj.view += 1
        obj.save()
        serialzier = self.get_serializer(obj)
        return Response(serialzier.data)


class HelpCategoryViewSet(ModelViewSet):
    queryset = HelpCategory.objects.all()
    serializer_class = serializers.HelpCategorySerializer


class PromoteViewSet(ModelViewSet):
    queryset = Promote.objects.all()
    serializer_class = serializers.PromoteSerializer
    http_method_names = ["get"]


class AdvertStatisticsFilter(django_filters.FilterSet):
    date = django_filters.DateTimeFromToRangeFilter(field_name="date")


class StatisticsView(ListAPIView):
    queryset = AdvertStatistics.objects.all()
    serializer_class = serializers.StatisticsSerializer
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filterset_class = AdvertStatisticsFilter
    ordering_fields = ["date"]
    ordering = ["date"]


class SubCategoryView(ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = serializers.SubCategorySerializer


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = serializers.TransactionListSerializer
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
        params = generate_sig(data, method)
        url = get_payment_details(params, method)
        return Response({**serializer.data, 'redirect_url': url})




