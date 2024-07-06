import json
from general import constants
from django.utils import timezone
from django.db import transaction
from rest_framework import serializers
from general.mixins import CustomSerializerErrorMessagesMixin
from trip.models import (
    Trip, Regency, TripInclude, 
    TripExclude, TripGallery, TripItinerary
)

class TripIncludeSerializer(CustomSerializerErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = TripInclude
        fields = ['id','item']       

class TripExcludeSerializer(CustomSerializerErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = TripExclude
        fields = ['id','item']

class TripItinerarySerializer(CustomSerializerErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = TripItinerary
        fields = ['id','day','time','activity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True

class TripGallerySerializer(CustomSerializerErrorMessagesMixin, serializers.ModelSerializer):
    image = serializers.ImageField(
        max_length=None,
        allow_empty_file=False,
        error_messages={
            'invalid': 'Harap upload file dengan format JPEG, PNG, dan GIF.'
        }
    )
    class Meta:
        model = TripGallery
        fields = ['id','image','title','description']

class TripSerializer(CustomSerializerErrorMessagesMixin, serializers.ModelSerializer):
    trip_includes = TripIncludeSerializer(many=True, required=True)
    trip_excludes = TripExcludeSerializer(many=True, required=True)
    trip_galleries = TripGallerySerializer(many=True, required=False)
    trip_itineraries = TripItinerarySerializer(many=True, required=True)
    slug = serializers.SlugField(read_only=True)
    regency_id = serializers.PrimaryKeyRelatedField(
        queryset=Regency.objects.all(),
        source='regency',
        write_only=True,
        required=True
    )

    class Meta:
        model = Trip
        fields = '__all__'
        read_only_fields = ['rate_avg']
        depth = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request', None)

        # set fields optional for patch
        if request and request.method in ['PATCH']:
            for field in self.fields:
                self.fields[field].required = False

    def validate_thumbnail(self, value):
        max_size = 2 * 1024 * 1024 # max 2 MB 
        if value and value.size > max_size:
            raise serializers.ValidationError(f"Ukuran file tidak boleh lebih dari {max_size / (1024 * 1024)} MB.")
        return value

    def validate(self, data):
        total_day = data.get('total_day', None)
        total_night = data.get('total_night', None)
        trip_date = data.get('trip_date', None)

        errors = {}
        errors.update(self._validate_negative_fields(data))

        if total_day and total_night:
            # example: 1d 2n is invalid
            if total_night > total_day:
                errors['total_night'] = "Jumlah malam tidak boleh melebihi jumlah hari."

            # example: 1day 3night is invalid
            if (total_day - total_night) > 1:
                errors['total_night'] = "Jumlah selisih hari dan malam terlalu banyak."

        if trip_date and trip_date < timezone.now().date():
            errors['trip_date'] = constants.ERROR_PAST_DATE_FIELD

        if errors:
            raise serializers.ValidationError(errors)
        
        return data

    def create(self, validated_data):
        with transaction.atomic():
            includes_data = validated_data.pop('trip_includes',[])
            excludes_data = validated_data.pop('trip_excludes',[])
            galleries_data = validated_data.pop('trip_galleries',[])
            itineraries_data = validated_data.pop('trip_itineraries',[])

            trip = Trip.objects.create(**validated_data)
            
            self.create_includes(trip, includes_data)
            self.create_excludes(trip, excludes_data)
            self.create_itineraries(trip, itineraries_data)
            self.create_galleries(trip, galleries_data)

        return trip
    
    def update(self, instance, validated_data):
        includes_data = validated_data.pop('trip_includes',[])
        excludes_data = validated_data.pop('trip_excludes',[])
        galleries_data = validated_data.pop('trip_galleries',[])
        itineraries_data = validated_data.pop('trip_itineraries',[])
        regency = validated_data.get('regency', None)
        
        with transaction.atomic():
            # unlink old thumbnail
            if 'thumbnail' in validated_data and instance.thumbnail:
                old_thumbnail = instance.thumbnail
                new_thumbnail = validated_data['thumbnail']

                if old_thumbnail != new_thumbnail:
                    instance.thumbnail.delete(save=False)

            if regency:
                instance.regency = regency

            # update the trip
            instance.__dict__.update(**validated_data)
            instance.save()

            # update relations
            if includes_data:
                instance.trip_includes.all().delete()
                self.create_includes(instance, includes_data)

            if excludes_data:
                instance.trip_excludes.all().delete()
                self.create_excludes(instance, excludes_data)

            if itineraries_data:
                instance.trip_itineraries.all().delete()
                self.create_itineraries(instance, itineraries_data)

            if galleries_data:
                instance.trip_galleries.all().delete()
                self.create_galleries(instance, galleries_data)
        return instance


    # split to reduce complexity
    def _validate_negative_fields(self, data):
        errors = {}
        for field, value in data.items():
            if field in ['total_day','total_night','price','min_member','max_member']:
                if value < 0:
                    errors[field] = constants.ERROR_NEGATIVE_FIELD
        return errors

    def create_includes(self, instance, includes_data):
        for include_data in includes_data:
            TripInclude.objects.create(trip=instance, **include_data)

    def create_excludes(self, instance, excludes_data):
        for exclude_data in excludes_data:
            TripExclude.objects.create(trip=instance, **exclude_data)

    def create_itineraries(self, instance, itineraries_data):
        for itinerary_data in itineraries_data:
            if 'activities' in itinerary_data:
                itinerary_data['activities'] = json.loads(itinerary_data['activities'])
            TripItinerary.objects.create(trip=instance, **itinerary_data)

    def create_galleries(self, instance, galleries_data):
        for gallery_data in galleries_data:
            TripGallery.objects.create(trip=instance, **gallery_data)