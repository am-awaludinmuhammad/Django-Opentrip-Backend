import os
import json
import logging
from trip.models import Trip
from datetime import datetime
from django.urls import reverse
from order.models import Review
from django.test import TestCase
from django.conf import settings
from rest_framework import status
from rest_framework.test import APIClient
from order.utils import calculate_trip_rate_avg
from rest_framework_simplejwt.tokens import AccessToken
from django.core.files.uploadedfile import SimpleUploadedFile
from general.factories import UserFactory, TripFactory, OrderFactory, BankFactory, ReviewFactory

logger = logging.getLogger('file')

class PaymentTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory(is_staff=False, is_superuser=False)
        self.user2 = UserFactory(is_staff=False, is_superuser=False)
        self.superuser = UserFactory(is_staff=True, is_superuser=True)

        self.user_token = AccessToken.for_user(self.user)
        self.superuser_token = AccessToken.for_user(self.superuser)

        self.trip = TripFactory()
        self.bank = BankFactory()
        self.order = OrderFactory(
            gross_amount=self.trip.price, 
            trip=self.trip, 
            user=self.user,
            status='success'
        )

        self.order2= OrderFactory(
            gross_amount=self.trip.price, 
            trip=self.trip, 
            user=self.user2,
            status='success'
        )

        self.image_path = os.path.join(settings.BASE_DIR,'test_image.png')

        with open(self.image_path, 'rb') as image_file:
            self.proof_image = SimpleUploadedFile(
                name='proof1.png',
                content=image_file.read(),
                content_type='image/png'
            )
        self.payment_data = {
            'order_id': self.order.id,
            'proof_date': datetime.now().date(),
            'bank_id': self.bank.id,
            'proof_image': self.proof_image,
        }

    def tearDown(self):
        Review.objects.all().delete()

    def test_create_review(self):
        url = reverse('review-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        data = {
            'order_id': self.order.id,
            'description': 'review description',
            'rate': 4
        }
        
        response = self.client.post(url, data, format='json')
        rendered_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('data', rendered_response)

        trip = Trip.objects.get(id=self.trip.id)
        self.assertEqual(trip.rate_avg, 4)

    def test_destroy_review(self):
        review = ReviewFactory(order=self.order)
        url = reverse('review-detail', args=[review.id])

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_destroy_review(self):
        review = ReviewFactory(order=self.order)
        url = reverse('review-detail', args=[review.id])

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_destroy_other_user_review(self):
        review = ReviewFactory(order=self.order2)
        url = reverse('review-detail', args=[review.id])

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_member_update_review(self):
        review = ReviewFactory(order=self.order, rate=5)

        trip = Trip.objects.get(id=self.order.trip.id)
        self.assertEqual(review.rate, 5)
        self.assertEqual(trip.rate_avg, calculate_trip_rate_avg(trip))

        url = reverse('review-detail', args=[review.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')

        data = {
            'rate': 4,
            'description': 'updated description',
        }
        
        response = self.client.patch(url, data, format='json')
        rendered_response = json.loads(response.content)

        trip = Trip.objects.get(id=review.order.trip.id)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', rendered_response)
        self.assertEqual(int(rendered_response['data']['rate']), int(data['rate']))
        self.assertEqual(trip.rate_avg, calculate_trip_rate_avg(trip))
        self.assertEqual(rendered_response['data']['description'], data['description'])

    def test_member_update_is_visible(self):
        review = ReviewFactory(order=self.order, rate=5)
        
        url = reverse('review-detail', args=[review.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')

        data = { 'is_visible': True }

        response = self.client.patch(url, data, format='json')
        rendered_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(rendered_response['data']['is_visible'], False)

    def test_admin_set_is_visible(self):
        review = ReviewFactory(order=self.order, rate=5, is_visible=False)

        url = reverse('review-set-visibility', args=[review.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        
        data = { 'is_visible': True }
        response = self.client.post(url, data, format='json')
        rendered_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(rendered_response['data']['is_visible'], data['is_visible'])

    def test_member_set_is_visible(self):
        review = ReviewFactory(order=self.order, rate=5, is_visible=False)

        url = reverse('review-set-visibility', args=[review.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        
        data = { 'is_visible': True }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)