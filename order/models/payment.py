from django.db import models
from order.models import Order
from django.db.models import Max
from django.utils import timezone
from general.choises import ORDER_PAYMENT_STATUS
from general.models import TimeStampedModel, Bank

class Payment(TimeStampedModel):
    confirmed_at = models.DateTimeField(null=True)
    payment_number = models.CharField(max_length=25)
    proof_date = models.DateField(null=True)
    proof_image = models.ImageField(upload_to='order/payment_proofs/')
    status = models.CharField(max_length=20, choices=ORDER_PAYMENT_STATUS, default='pending')
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='payments')
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')

    class Meta:
        ordering = ['created_at']
        db_table = 'payments'

    def __str__(self):
        return f'Payment id: {self.id}, order id: {self.order.id}'
    
    def save(self, *args, **kwargs):
        self.payment_number = self.generate_payment_number()
        super(Payment, self).save(*args, **kwargs)

    @staticmethod
    def generate_payment_number():
        today = timezone.now()
        year = today.strftime('%Y')
        month = today.strftime('%m')
        day = today.strftime('%d')
        
        last_order = Payment.objects.aggregate(Max('id'))['id__max'] or 0
        sequential_number = last_order + 1
        
        return f'PAYMENT_{year}_{month}_{day}_{sequential_number:04d}'