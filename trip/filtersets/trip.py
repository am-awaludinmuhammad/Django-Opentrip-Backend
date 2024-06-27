import django_filters
from trip.models import Trip

class TripFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    min_trip_date = django_filters.DateFilter(field_name='trip_date', lookup_expr='gte')
    max_trip_date = django_filters.DateFilter(field_name='trip_date', lookup_expr='lte')

    class Meta:
        model = Trip
        fields = [
            'price',
            'min_price',
            'max_price',
            'total_day',
            'total_night',
            'trip_date',
            'min_trip_date',
            'max_trip_date',
        ]