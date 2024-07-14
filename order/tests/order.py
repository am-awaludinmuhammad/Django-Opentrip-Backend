import json
import logging
from trip.models import Trip
from order.models import Order
from django.urls import reverse
from account.models import User
from django.test import TestCase
from rest_framework import status
from trip.models import Province,Regency
from datetime import datetime, timedelta
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

logger = logging.getLogger('file')

class CreateOrderTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(email='usertest@test.com', password='password', name='usertest')
        self.user_token = AccessToken.for_user(self.user)

        self.superuser = User.objects.create_superuser(email='superusertest@test.com', password='superpassword', name='superusertest')
        self.superuser_token = AccessToken.for_user(self.superuser)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')

        self.province = Province.objects.create(name='test province')
        self.regency = Regency.objects.create(name='test regency', province=self.province)

        self.today = datetime.now().date()
        self.date_after_7_days = self.today + timedelta(days=7)
        self.date_before_7_days = self.today - timedelta(days=7)
        self.trip_data = {
            'regency_id': self.regency.id,
            'name': 'test trip',
            'total_day': 3,
            'total_night': 2,
            'description': 'test description',
            'price': 850000,
            'terms': 'test terms',
            'meet_point': 'test meet pont',
            'trip_date': self.date_after_7_days,
            'min_member': 1,
            'max_member': 10,
            'trip_includes[0][item]':'test include 1',
            'trip_excludes[0][item]':'test exclude 1',
            'trip_itineraries[0][day]':1,
            'trip_itineraries[0][time]':'05:00:00',
            'trip_itineraries[0][activity]':'activity 1',
        }
        
        url = reverse('trip-list')
        response = self.client.post(url, self.trip_data, format='multipart')
        rendered_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('data', rendered_response)
        self.trip = Trip.objects.get(pk=rendered_response['data']['id'])    

    def tearDown(self):
        Order.objects.all().delete()
        Trip.objects.all().delete()

    def test_create_order_unauthorized(self):
        url = reverse('order-list')
        self.client.credentials()
        data = {
            'trip_id': self.trip.id
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order(self):
        url = reverse('order-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        data = {
            'trip_id': self.trip.id
        }
        response = self.client.post(url, data, format='json')
        rendered_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('data', rendered_response)
        self.assertIn('id', rendered_response['data'])
        self.assertIn('trip', rendered_response['data'])

    def test_update_order_not_allowed(self):
        url = reverse('order-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        data = {
            'trip_id': self.trip.id
        }
        response = self.client.post(url, data, format='json')
        rendered_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', rendered_response['data'])
        order_id = rendered_response['data']['id']
        
        url = reverse('order-detail', args=[order_id])
        data = {
            'gross_amount': 0
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_order_not_allowed(self):
        url = reverse('order-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        data = {
            'trip_id': self.trip.id
        }
        response = self.client.post(url, data, format='json')
        rendered_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', rendered_response['data'])
        order_id = rendered_response['data']['id']
        
        url = reverse('order-detail', args=[order_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
