import logging
from rest_framework import serializers
from order.models import Order, Review
from account.utils import user_is_admin
from order.serializers import OrderSerializer
from rest_framework.exceptions import PermissionDenied

logger = logging.getLogger('file')

class SetReviewVisibilitySerializer(serializers.ModelSerializer):
    is_visible = serializers.BooleanField(required=True)
    class Meta:
        model = Review
        fields = ['id', 'is_visible']
        read_only_fields = ['id']

class ReviewSerializer(serializers.ModelSerializer):
    order_id = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(),
        write_only=True,
        required=True
    )
    order = OrderSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'description',
            'is_visible',
            'rate',
            'order_id',
            'order',
            'id',
        ]
        read_only_fields = ['id', 'order', 'is_visible']
        depth = 1

    def validate_rate(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError("Masukkan nilai antara 1 - 5")

        return value

    def validate_order_id(self, value):
        request = self.context.get('request')

        # check order review exists
        if Review.objects.filter(order=value).exists():
            raise serializers.ValidationError("Data ulasan untuk order ini sudah ada")
        
        # check status
        order = Order.objects.get(pk=value.id)
        if not order:
            raise serializers.ValidationError("Data order tidak ditemukan")

        if order and not user_is_admin(request.user) and order.user != request.user:
            raise PermissionDenied("Anda tidak diperkenankan memberikan ulasan untuk pesanan ini.")

        if order and order.status != 'success':
            raise serializers.ValidationError("Order belum selesai. Tidak diperkenankan mengisi ulasan")

        return value

    def create(self, validated_data):
        validated_data['order'] = validated_data.pop('order_id')
        return Review.objects.create(**validated_data)