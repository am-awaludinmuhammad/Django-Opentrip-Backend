import logging
from django.utils import timezone
from django.db.models import Max, Avg

logger = logging.getLogger('file')

def generate_order_number():
    from order.models import Order
    today = timezone.now()
    year = today.strftime('%Y')
    month = today.strftime('%m')
    day = today.strftime('%d')
    
    # Get the last order sequence number
    last_order = Order.objects.aggregate(Max('id'))['id__max'] or 0
    sequential_number = last_order + 1
    
    return f'ORDER_{year}_{month}_{day}_{sequential_number:04d}'

def calculate_trip_rate_avg(trip_instance):
    from order.models import Order, Review

    
    orders = Order.objects.filter(trip=trip_instance)
    reviews = Review.objects.filter(order__in=orders)

    average_rating = reviews.aggregate(Avg('rate'))['rate__avg'] or 0

    trip_instance.rate_avg = average_rating
    trip_instance.save()

    return average_rating