from rest_framework_simplejwt.tokens import RefreshToken
import json
from account.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase,APIClient

class AuthTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'testmail@test.com',
            'name': 'testname',
            'password': 'password',
            'password_confirm':'password'
        }
        self.user = User.objects.create_user(email=self.user_data['email'], password=self.user_data['password'], name=self.user_data['name'])
        
    def tearDown(self):
        User.objects.all().delete()

    def test_register_user(self):
        url = reverse('user-list')
        data = {
            'email': 'testmail1@test.com',
            'name': 'testname',
            'password': 'password',
            'password_confirm':'password'
        }
        response = self.client.post(url, data, format='json')
        rendered_response = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('data', rendered_response)

        user = User.objects.get(pk=rendered_response['data']['id'])
        self.assertEqual(user.name, self.user_data['name'])

    def test_register_user_bad_request(self):
        url = reverse('user-list')
        data = {
            'name': self.user_data['name'],
        }
        response = self.client.post(url, data, format='json')
        rendered_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', rendered_response)
        self.assertIn('email', rendered_response['errors'])
        self.assertIn('password', rendered_response['errors'])
        self.assertIn('password_confirm', rendered_response['errors'])

    def test_login(self):
        url = reverse('token_obtain_pair')
        data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }

        response = self.client.post(url, data, format='json')
        rendered_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', rendered_response)
        self.assertIn('access', rendered_response['data'])
        self.assertIn('refresh', rendered_response['data'])

    def test_login_wrong_email(self):
        url = reverse('token_obtain_pair')
        data = {
            'email': 'wrongemail@test.com',
            'password': self.user_data['password']
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_login_wrong_password(self):
        url = reverse('token_obtain_pair')
        data = {
            'email': self.user_data['email'],
            'password': 'wrongpassword'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_password(self):
        url = reverse('token_refresh')
        refresh = RefreshToken.for_user(self.user)
        data = {
            'refresh': str(refresh)
        }

        response = self.client.post(url, data, format='json')
        rendered_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', rendered_response)
        self.assertIn('access', rendered_response['data'])