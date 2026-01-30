from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('users-register')
        self.login_url = reverse('users-login')
        self.logout_url = reverse('users-logout')
        self.me_url = reverse('users-me')
        self.update_me_url = reverse('users-update-me')
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123',
            'phone': '1234567890',
            'money_preference': 'USD'
        }

    def test_registration(self):
        """
        Ensure we can create a new user object.
        """
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_login(self):
        """
        Ensure we can login with a registered user and get tokens.
        """
        # First register
        self.client.post(self.register_url, self.user_data, format='json')
        
        # Then login
        login_data = {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }
        response = self.client.post(self.login_url, login_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)

    def test_logout(self):
        """
        Ensure we can logout (blacklist refresh token).
        """
        # Register and Login to get tokens
        self.client.post(self.register_url, self.user_data, format='json')
        login_data = {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }
        login_response = self.client.post(self.login_url, login_data, format='json')
        access_token = login_response.data['access']
        refresh_token = login_response.data['refresh']

        # Authenticate for logout
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        # Logout
        response = self.client.post(self.logout_url, {'refresh': refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_me(self):
        """
        Ensure we can get the current user profile.
        """
        self.client.post(self.register_url, self.user_data, format='json')
        login_data = {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }
        login_response = self.client.post(self.login_url, login_data, format='json')
        access_token = login_response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.me_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user_data['username'])

    def test_update_me(self):
        """
        Ensure we can update the current user profile.
        """
        self.client.post(self.register_url, self.user_data, format='json')
        login_data = {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }
        login_response = self.client.post(self.login_url, login_data, format='json')
        access_token = login_response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        update_data = {
            'phone': '0987654321',
            'money_preference': 'EUR'
        }
        response = self.client.put(self.update_me_url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone'], update_data['phone'])
        self.assertEqual(response.data['money_preference'], update_data['money_preference'])
