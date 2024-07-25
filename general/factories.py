import factory
import datetime
from account.models import User
from general.models import Bank
from order.models import Order, Payment, Review
from factory.django import DjangoModelFactory
from trip.models import (Province, 
                         Regency, 
                         Trip, 
                         TripExclude, 
                         TripInclude, 
                         TripItinerary, 
                         TripGallery)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f'user{n}@mail.com')
    password = factory.PostGenerationMethodCall('set_password', 'defaultpassword')

class ProvinceFactory(DjangoModelFactory):
    class Meta:
        model = Province
    
class RegencyFactory(DjangoModelFactory):
    class Meta:
        model = Regency
    
    province = factory.SubFactory(ProvinceFactory)

class TripGalleryFactory(DjangoModelFactory):
    class Meta:
        model = TripGallery

class TripIncludeFactory(DjangoModelFactory):
    class Meta:
        model = TripInclude

class TripExcludeFactory(DjangoModelFactory):
    class Meta:
        model = TripExclude

class TripItineraryFactory(DjangoModelFactory):
    class Meta:
        model = TripItinerary

class TripFactory(DjangoModelFactory):
    class Meta:
        model = Trip

    total_day = 1
    min_member = 5
    total_night = 1
    max_member = 10
    price = "100000.00"
    name = 'default name'
    terms = 'default terms'
    trip_date = datetime.datetime.now().date()
    regency = factory.SubFactory(RegencyFactory)

class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    trip = factory.SubFactory(TripFactory)
    user = factory.SubFactory(UserFactory)

class BankFactory(DjangoModelFactory):
    class Meta:
        model = Bank

class PaymentFactory(DjangoModelFactory):
    class Meta:
        model = Payment

    proof_date = datetime.datetime.now().date()
    proof_image = 'image.png'
    order = factory.SubFactory(OrderFactory)
    bank = factory.SubFactory(BankFactory)
    confirmed_at = None

class ReviewFactory(DjangoModelFactory):
    class Meta:
        model = Review

    order = factory.SubFactory(OrderFactory)
    