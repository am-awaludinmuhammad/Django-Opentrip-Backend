import logging
from trip.models import Trip
from order.models import Order
from rest_framework import serializers
from trip.serializers import TripSerializer
from account.serializers import UserSerializer
from trip.serializers.basic import BasicTripReadSerializer

logger = logging.getLogger('file')

class OrderDetailSerialzier(serializers.ModelSerializer):
    trip = TripSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    trip_id = serializers.PrimaryKeyRelatedField(
        queryset=Trip.objects.all(),
        write_only=True,
        required=True
    )
    trip = BasicTripReadSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    payment = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = [
            'user',
            'trip',
            'status',
            'trip_date',
            'created_at',
            'updated_at',
            'order_number',
            'gross_amount',
            'payment',
        ]
        depth=1

    def get_payment(self, obj):
        if hasattr(obj, 'payment'):
            from order.serializers import PaymentSerializer
            return PaymentSerializer(obj.payment).data
        return None

    def create(self, validated_data):
        request = self.context.get('request')
        trip = validated_data.pop('trip_id')

        return Order.objects.create(**{
            'trip': trip,
            'gross_amount': trip.price,
            'trip_date': trip.trip_date,
            'user': request.user
        })