from order.models import Payment
from account.utils import user_is_admin
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins, status
from general.pagination import CustomPageNumberPagination
from rest_framework.parsers import MultiPartParser, JSONParser
from order.serializers import PaymentSerializer, PaymentConfirmSerializer

class PaymentViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    pagination_class = CustomPageNumberPagination
    parser_classes = [MultiPartParser, JSONParser]

    @extend_schema(request=PaymentConfirmSerializer, responses=PaymentConfirmSerializer)
    def confirm(self, request, *args, **kwargs):

        if not user_is_admin(request.user):
            return Response({'detail': 'Forbidden'}, status.HTTP_403_FORBIDDEN)

        payment = self.get_object()
        serializer = PaymentConfirmSerializer(payment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)