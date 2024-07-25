import logging

from django.db import models
from order.models import Order
from general.models import TimeStampedModel
from order.utils import calculate_trip_rate_avg

logger = logging.getLogger('file')

class Review(TimeStampedModel):
    description = models.TextField(null=True)
    is_visible = models.BooleanField(default=False)
    rate = models.IntegerField(default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        ordering = ['created_at']
        db_table = 'reviews'

    def save(self, *args, **kwargs):
        super(Review, self).save(*args, **kwargs)
        calculate_trip_rate_avg(self.order.trip)

    @property
    def user(self):
        return self.order.user