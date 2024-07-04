from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status
import json
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from account.models import User

class UserTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='usertest@test.com', password='password', name='usertest')
        self.superuser = User.objects.create_superuser(email='superusertest@test.com', password='superpassword', name='superusertest')

        self.user_token = AccessToken.for_user(self.user)
        self.superuser_token = AccessToken.for_user(self.superuser)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')

    def tearDown(self):
        User.objects.all().delete()

    def test_fetch_users(self):
        url = reverse('user-list')
        response = self.client.get(url, format='json')
        rendered_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', rendered_response)
    
    def test_get_active_users(self):        
        extra_fields = {
            'is_active': False
        }
        User.objects.create_user(email='inactive@test.com', password='password', name='inactive user', **extra_fields)
        
        url = reverse('user-list')
        params = {
            'is_active': True
        }
        response = self.client.get(url, params, format='json')
        rendered_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', rendered_response)
        self.assertIn('count', rendered_response['data'])
        self.assertEqual(rendered_response['data']['count'], 2)
    
    def test_fetch_user_forbidden(self):
        url = reverse('user-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        response = self.client.get(url, format='json')
        rendered_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('errors', rendered_response)

    def test_patch_user(self):
        url = reverse('user-detail', args=[self.user.id])
        data = {
            'name': 'updated name',
            'phone': '6286123123'
        }
        
        response = self.client.patch(url, data, format='json')
        rendered_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', rendered_response)

        user = User.objects.get(pk=self.user.id)
        self.assertEqual(user.name, data['name'])
        self.assertEqual(user.phone, data['phone'])

    def test_destroy_user(self):
        url = reverse('user-detail', args=[self.user.id])
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)