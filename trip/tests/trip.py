import os
import json
import logging
from trip.models import Trip
from django.urls import reverse
from account.models import User
from trip.models import Province,Regency
from django.test import TestCase
from django.conf import settings
from rest_framework import status
logger = logging.getLogger('file')
from datetime import datetime, timedelta
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from django.core.files.uploadedfile import SimpleUploadedFile

class TripTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.superuser = User.objects.create_superuser(email='superusertest@test.com', password='superpassword', name='superusertest')
        self.superuser_token = AccessToken.for_user(self.superuser)

        self.user = User.objects.create_user(email='usertest@test.com', password='password', name='usertest')
        self.user_token = AccessToken.for_user(self.user)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')

        self.big_image_path = os.path.join(settings.BASE_DIR,'big_image.jpg')
        self.image_path = os.path.join(settings.BASE_DIR,'test_image.png')
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

        new_data = self.trip_data
        new_data['name'] = 'test trip slug'
        response = self.client.post(reverse('trip-list'), self.trip_data, format='multipart')
        rendered_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('data', rendered_response)
        self.trip = rendered_response['data']

    def tearDown(self):
        Trip.objects.all().delete()
        User.objects.all().delete()
    
    def test_create_trip_forbidden(self):
        url = reverse('trip-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        response = self.client.post(url, self.trip_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_required_fields(self):
        url = reverse('trip-list')
        required_fields = [
            'name',
            'total_day',
            'total_night',
            'description',
            'price',
            'terms',
            'meet_point',
            'trip_date',
            'min_member',
            'max_member',
            'regency_id',
            'trip_includes',
            'trip_excludes',
            'trip_itineraries',
        ]
        response = self.client.post(url, {}, format='multipart')
        rendered_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', rendered_response)
        for field in required_fields:
            self.assertIn(field, rendered_response['errors'])
    
    def test_invalid_trip_includes(self):
        data = self.trip_data
        data.pop('trip_includes[0][item]',[])
        data['trip_includes[0][wrongkey]'] = 1
    
        url = reverse('trip-list')

        response = self.client.post(url, data, format='multipart')
        rendered_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', rendered_response)
        self.assertIn('trip_includes', rendered_response['errors'])
        self.assertIn('item', rendered_response['errors']['trip_includes'][0])

    def test_invalid_trip_excludes(self):
        data = self.trip_data
        data.pop('trip_excludes[0][item]',[])
        data['trip_excludes[0][wrongkey]'] = 1
        url = reverse('trip-list')

        response = self.client.post(url, data, format='multipart')
        rendered_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', rendered_response)
        self.assertIn('trip_excludes', rendered_response['errors'])
        self.assertIn('item', rendered_response['errors']['trip_excludes'][0])

    def test_invalid_trip_itineraries(self):
        data = self.trip_data
        data.pop('trip_itineraries[0][day]',[])
        data.pop('trip_itineraries[0][time]',[])

        data['trip_itineraries[0][day]'] = 'invalid'
        data['trip_itineraries[0][time]'] = 'invalid'
        url = reverse('trip-list')

        response = self.client.post(url, data, format='multipart')
        rendered_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', rendered_response)
        self.assertIn('trip_itineraries', rendered_response['errors'])
        self.assertIn('day', rendered_response['errors']['trip_itineraries'][0])
        self.assertIn('time', rendered_response['errors']['trip_itineraries'][0])
    
    def test_invalid_trip_date_type(self):
        data = self.trip_data
        data['trip_date'] = 'invalid'
        url = reverse('trip-list')

        response = self.client.post(url, data, format='multipart')
        rendered_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', rendered_response)
        self.assertIn('trip_date', rendered_response['errors'])
    
    def test_invalid_trip_date_past(self):
        data = self.trip_data
        data['trip_date'] = self.date_before_7_days
        url = reverse('trip-list')

        response = self.client.post(url, data, format='multipart')
        rendered_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', rendered_response)
        self.assertIn('trip_date', rendered_response['errors'])
    
    def test_total_night_gt_total_day(self):
        data = self.trip_data
        data['total_day'] = 2
        data['total_night'] = 3
        url = reverse('trip-list')

        response = self.client.post(url, data, format='multipart')
        rendered_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', rendered_response)
        self.assertIn('total_night', rendered_response['errors'])

    def test_invalid_total_day_night_combination(self):
        data = self.trip_data
        data['total_day'] = 6
        data['total_night'] = 3
        url = reverse('trip-list')

        response = self.client.post(url, data, format='multipart')
        rendered_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', rendered_response)
        self.assertIn('total_night', rendered_response['errors'])

    def test_create_trip_without_thumbnail(self):
        url = reverse('trip-list')

        response = self.client.post(url, self.trip_data, format='multipart')
        rendered_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('data', rendered_response)

    def test_create_trip_with_thumbnail(self):
        url = reverse('trip-list')
        data = self.trip_data
        with open(self.image_path, 'rb') as image_file:
            data['thumbnail'] = SimpleUploadedFile(
                name='thumnail.png',
                content=image_file.read(),
                content_type='image/png'
            )
        response = self.client.post(url, self.trip_data, format='multipart')
        rendered_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('data', rendered_response)

    def test_create_trip_big_size_thumbnail(self):
        url = reverse('trip-list')
        data = self.trip_data
        with open(self.big_image_path, 'rb') as image_file:
            data['thumbnail'] = SimpleUploadedFile(
                name='thumnail.png',
                content=image_file.read(),
                content_type='image/png'
            )
        response = self.client.post(url, self.trip_data, format='multipart')
        rendered_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', rendered_response)
        self.assertIn('thumbnail', rendered_response['errors'])

    def test_create_trip_minus_value(self):
        url = reverse('trip-list')
        data = self.trip_data
        data['total_day'] = -1
        data['price'] = -1
        data['total_night'] = -1

        response = self.client.post(url, data, format='multipart')
        rendered_response = json.loads(response.content)

        logger.info(rendered_response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', rendered_response)
        self.assertIn('total_day', rendered_response['errors'])
        self.assertIn('total_night', rendered_response['errors'])
        self.assertIn('price', rendered_response['errors'])

    def test_trip_detail_by_id(self):
        url = reverse('trip-detail', args=[self.trip['id']])
        response = self.client.get(url)
        rendered_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', rendered_response)

    def test_trip_detail_by_slug(self):
        url = reverse('trip-detail', args=[self.trip['slug']])
        response = self.client.get(url)
        rendered_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', rendered_response)
        self.assertEqual(rendered_response['data']['id'], self.trip['id'])

    def test_patch_trip(self):
        url = reverse('trip-detail', args=[self.trip['id']])
        data = {'name': 'updated trip'}
        response = self.client.patch(url, data, format='multipart')
        rendered_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', rendered_response)
        self.assertEqual(rendered_response['data']['name'], data['name'])

    def test_delete_trip(self):
        url = reverse('trip-detail', args=[self.trip['id']])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
