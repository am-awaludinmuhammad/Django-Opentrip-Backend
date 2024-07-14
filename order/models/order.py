from django.db import models
from trip.models import Trip
from account.models import User
from django.db.models import Max
from django.utils import timezone
from general.models import TimeStampedModel
from general.choises import ORDER_PAYMENT_STATUS

class Order(TimeStampedModel):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='orders')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    gross_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_PAYMENT_STATUS, default='pending')
    order_number = models.CharField(max_length=25)
    trip_date = models.DateField(null=True)

    class Meta:
        ordering = ['created_at']
        db_table = 'orders'

    def __str__(self):
        return f'Order of Trip {self.trip.name}'
    
    def save(self, *args, **kwargs):
        self.order_number = self.generate_order_number()
        super(Order, self).save(*args, **kwargs)

    @staticmethod
    def generate_order_number():
        today = timezone.now()
        year = today.strftime('%Y')
        month = today.strftime('%m')
        day = today.strftime('%d')
        
        last_order = Order.objects.aggregate(Max('id'))['id__max'] or 0
        sequential_number = last_order + 1
        
        return f'ORDER_{year}_{month}_{day}_{sequential_number:04d}'