import json
from general import constants
from django.utils import timezone
from django.db import transaction
from rest_framework import serializers
from general.mixins import CustomSerializerErrorMessagesMixin
from trip.models import Trip

class BasicTripReadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Trip
        fields = [
            'id',
            'name',
            'total_day',
            'total_night',
            'slug',
            'trip_date',
        ]