import os
import json
import logging
from django.urls import reverse
from account.models import User
from django.conf import settings
from rest_framework import status
logger = logging.getLogger('django')
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from django.core.files.uploadedfile import SimpleUploadedFile

class ProfileTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(email='usertest@test.com', password='password', name='usertest')
        self.user_token = AccessToken.for_user(self.user)
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        self.image_path = os.path.join(settings.BASE_DIR,'test_image.png')

    def tearDown(self): 
        User.objects.all().delete()

    def test_unauthorized(self):
        url = reverse('profile')
        self.client.credentials(HTTP_AUTHORIZATION=None)
        response = self.client.get(url)        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile(self):
        url = reverse('profile')
        response = self.client.get(url)
        rendered_response = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', rendered_response)
        self.assertEqual(rendered_response['data']['id'], self.user.id)

    def test_patch_update(self):
        url = reverse('profile')
        data = {
            'name': 'updated'
        }
        response = self.client.patch(url, data, format='multipart')
        rendered_response = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', rendered_response)
        self.assertEqual(rendered_response['data']['name'], data['name'])

    def test_update_avatar(self):
        url = reverse('profile')
        with open(self.image_path, 'rb') as image_file:
            image = SimpleUploadedFile(
                name='test_image.png',
                content=image_file.read(),
                content_type='image/png'
            )
        response = self.client.patch(url, {'avatar': image}, format='multipart')
        rendered_response = json.loads(response.content)

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', rendered_response)
        self.assertTrue(self.user.avatar is not None)