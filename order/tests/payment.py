import os
import json
import logging
from django.urls import reverse
from django.test import TestCase
from django.conf import settings
from rest_framework import status
from order.models import Payment
from datetime import datetime
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from django.core.files.uploadedfile import SimpleUploadedFile
from general.factories import UserFactory, TripFactory, OrderFactory, BankFactory, PaymentFactory

logger = logging.getLogger('file')

class PaymentTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory(is_staff=False, is_superuser=False)
        self.user2 = UserFactory(is_staff=False, is_superuser=False)
        self.superuser = UserFactory(is_staff=True, is_superuser=True)

        self.user_token = AccessToken.for_user(self.user)
        self.user2_token = AccessToken.for_user(self.user2)
        self.superuser_token = AccessToken.for_user(self.superuser)

        self.trip = TripFactory()
        self.bank = BankFactory()
        self.order = OrderFactory(
            gross_amount=self.trip.price, 
            trip=self.trip, 
            user=self.user)

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
        Payment.objects.all().delete()

    def test_payment(self):
        url = reverse('payment')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')

        response = self.client.post(url, self.payment_data, format='multipart')
        rendered_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('data', rendered_response)

    def test_payment_bad_request(self):
        url = reverse('payment')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        
        response = self.client.post(url, {}, format='multipart')
        rendered_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', rendered_response)
        self.assertIn('order_id', rendered_response['errors'])
        self.assertIn('proof_date', rendered_response['errors'])
        self.assertIn('bank_id', rendered_response['errors'])

    def test_create_other_user_payment_forbidden(self):
        url = reverse('payment')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user2_token}')

        response = self.client.post(url, self.payment_data, format='multipart')
        rendered_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('errors', rendered_response)

    def test_payment_duplicate(self):
        url = reverse('payment')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')

        PaymentFactory(order=self.order, bank=self.bank)

        response = self.client.post(url, self.payment_data, format='multipart')
        rendered_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', rendered_response)
        self.assertIn('order_id', rendered_response['errors'])

    def test_payment_confirmation(self):
        payment = PaymentFactory(order=self.order, bank=self.bank)

        url = reverse('payment-confirm', args=[payment.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')

        response = self.client.post(url, self.payment_data, format='multipart')
        rendered_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', rendered_response)

        payment = Payment.objects.get(pk=payment.id)
        self.assertEqual(payment.order.status, 'success')

    def test_payment_confirmation_forbidden(self):
        payment = PaymentFactory(order=self.order, bank=self.bank)

        url = reverse('payment-confirm', args=[payment.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')

        response = self.client.post(url, self.payment_data, format='multipart')
        rendered_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('errors', rendered_response)
