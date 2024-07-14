from order.models import Order
from rest_framework import permissions
from account.utils import user_is_admin
from rest_framework import viewsets, mixins
from general.pagination import CustomPageNumberPagination
from order.serializers import OrderSerializer, OrderDetailSerialzier
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    search_fields = ['trip__name', 'status']
    filterset_fields = ['created_at','status','trip__trip_date']

    def get_queryset(self):
        user = self.request.user
        trip_date = self.request.query_params.get('trip_date')
        min_trip_date = self.request.query_params.get('min_trip_date')
        max_trip_date = self.request.query_params.get('max_trip_date')
        min_amount = self.request.query_params.get('min_amount')
        max_amount = self.request.query_params.get('max_amount')

        queryset = super().get_queryset()

        if user_is_admin(user):
            queryset = queryset.all()
        else:
            queryset = queryset.filter(user=user)

        if trip_date:
            queryset = queryset.filter(trip__trip_date=trip_date)
        if min_trip_date:
            queryset = queryset.filter(trip_date__gte=min_trip_date)
        if max_trip_date:
            queryset = queryset.filter(trip_date__lte=max_trip_date)
        if min_amount:
            queryset = queryset.filter(gross_amount__gte=min_amount)
        if max_amount:
            queryset = queryset.filter(gross_amount__lte=max_amount)

        return queryset

    def get_object(self):
        user = self.request.user
        queryset =  self.get_queryset()

        if user_is_admin(user):
            return queryset.get(pk=int(self.kwargs.get('pk')))

        return queryset.get(pk=int(self.kwargs.get('pk')), user=user)
    
    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return OrderDetailSerialzier

        return super().get_serializer_class()