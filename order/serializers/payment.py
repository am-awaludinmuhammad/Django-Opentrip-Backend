import logging
import datetime
from django.db import transaction
from general.models import Bank
from rest_framework import serializers
from order.models import Order, Payment
from account.utils import user_is_admin
from general.serializers import BankSerializer
from rest_framework.exceptions import PermissionDenied

logger = logging.getLogger('file')

class PaymentConfirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'confirmed_at']
        read_only_fields = ['id', 'confirmed_at']
    
    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.confirmed_at = datetime.datetime.now()
            instance.status = 'success'
            instance.save()

            order = instance.order
            order.status = 'success'
            order.save()
            
        return instance

class PaymentSerializer(serializers.ModelSerializer):
    bank_id = serializers.PrimaryKeyRelatedField(
        queryset=Bank.objects.all(),
        write_only=True,
        required=True
    )
    order_id = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(),
        write_only=True,
        required=True
    )
    proof_image = serializers.ImageField(required=True)
    proof_date = serializers.DateField(required=True)
    bank = BankSerializer(many=False, read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id',
            'bank',
            'status',
            'bank_id',
            'order_id',
            'created_at',
            'updated_at',
            'proof_date',
            'proof_image',
            'confirmed_at',
            'payment_number',
        ]
        read_only_fields = [
            'confirmed_at','payment_number','status','bank'
        ]
        depth=1

    def validate_order_id(self, value):
        request = self.context.get('request')

        if not user_is_admin(request.user) and value.user != request.user:
            raise PermissionDenied("Anda tidak diperkenankan melakukan pembayaran untuk pesanan ini.")
        
        if Payment.objects.filter(order=value).exists():
            raise serializers.ValidationError("Data pembayaran sudah ada untuk pesanan ini.")
        return value

    def create(self, validated_data):
        validated_data['bank'] = validated_data.pop('bank_id')
        validated_data['order'] = validated_data.pop('order_id')

        return Payment.objects.create(**validated_data)