from django.db.models import Max
from django.utils import timezone
from order.models import Order

def generate_order_number():
    today = timezone.now()
    year = today.strftime('%Y')
    month = today.strftime('%m')
    day = today.strftime('%d')
    
    # Get the last order sequence number
    last_order = Order.objects.aggregate(Max('id'))['id__max'] or 0
    sequential_number = last_order + 1
    
    return f'ORDER_{year}_{month}_{day}_{sequential_number:04d}'