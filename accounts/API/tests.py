from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken

class TestUserRegisterApi(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="tester", password='tester')  # nosec B106
        self.token = RefreshToken.for_user(self.user)
        self.auth_header = {'HTTP_AUTHORIZATION': f'Bearer {self.token.access_token}'}
        self.register_url = reverse('user-register')

    def test_register_user_success(self):
        data = {
            'username': 'newuser',
            'password': 'securepassword123',
            'email': 'test@test.com',
        }
        response = self.client.post(self.register_url, data, format='json')

        user = User.objects.get(username=data['username'])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], data['username'])
        self.assertTrue(check_password(data['password'], user.password))

    def test_register_user_existing_username(self):
        data = {
            'username': 'tester',
            'password': 'newpassword123',
            'email': 'test@test.com',

        }
        response = self.client.post(self.register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'The user with the given login already exists.')

    def test_register_user_missing_username(self):
        data = {
            'password': 'securepassword123',
            'email': 'unknown@test.com',

        }
        response = self.client.post(self.register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_register_user_missing_password(self):
        data = {
            'username': 'newuserabc',
            'email': 'test@test.com',

        }
        response = self.client.post(self.register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_register_user_missing_email(self):
        data = {
            'username': 'newuserxyz',
            'password': 'securepassword123',

        }
        response = self.client.post(self.register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)