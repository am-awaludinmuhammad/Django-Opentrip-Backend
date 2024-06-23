from django.db import models
from general.models import TimeStampedModel

class Trip(TimeStampedModel):
    name = models.CharField(max_length=255)
    total_day = models.IntegerField()
    total_night = models.IntegerField()
    thumbnail = models.ImageField(upload_to='trip/thumbnails/', null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    terms = models.TextField()
    meet_point = models.CharField(max_length=255)
    trip_date = models.DateField()
    is_active = models.BooleanField(default=True)
    min_member = models.IntegerField()
    max_member = models.IntegerField()
    rate_avg = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    regency = models.ForeignKey('trip.Regency', on_delete=models.CASCADE, related_name='trips')

    class Meta:
        db_table = 'trips'

    def __str__(self):
        return self.name

class TripInclude(TimeStampedModel):
    item = models.TextField()
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='trip_includes')
    
    class Meta:
        db_table = 'trip_includes'

    def __str__(self):
        return self.item

class TripExclude(TimeStampedModel):
    item = models.TextField()
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='trip_excludes')

    class Meta:
        db_table = 'trip_excludes'

    def __str__(self):
        return self.item

class TripItinerary(TimeStampedModel):
    day = models.IntegerField()
    time_start = models.TimeField()
    time_end = models.TimeField()
    activities = models.JSONField()
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='trip_itineraries')

    class Meta:
        db_table = 'trip_itineraries'

    def __str__(self):
        return f"Hari ke-{self.day} {self.trip.name}"
    
class TripGallery(TimeStampedModel):
    image = models.ImageField(upload_to='trip/galleries/')
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='trip_galleries')
    
    class Meta:
        db_table = 'trip_galleries'
        
    def __str__(self):
        return self.description
    
    def delete(self, *args, **kwargs):
        # Optionally unlink the file from the storage
        self.image.delete(save=False)
        super().delete(*args, **kwargs)