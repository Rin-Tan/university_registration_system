from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from django.urls import reverse

class LoginAPITests(APITestCase):
    
    def setUp(self):
        self.username = 'testuser'
        self.password = 'StrongPass123'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )
        self.login_url = reverse('token_obtain_pair')
        
        self.valid_payload = {
            'username': self.username,
            'password': self.password
        }
        
        self.invalid_payload = {
            'username': self.username,
            'password': 'wrongpassword'
        }

    def test_successful_login_returns_tokens(self):
        """
        تست می‌کند که لاگین با اعتبارنامه صحیح، کد 200 و توکن‌های access/refresh را برمی‌گرداند.
        """
        response = self.client.post(self.login_url, self.valid_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_with_incorrect_password_fails(self):
        """
        تست می‌کند که لاگین با رمز عبور اشتباه، با کد 401 Unauthorized شکست می‌خورد.
        """
        response = self.client.post(self.login_url, self.invalid_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        self.assertNotIn('access', response.data)

    def test_login_with_nonexistent_user_fails(self):
        """
        تست می‌کند که اگر نام کاربری وجود نداشته باشد، لاگین شکست می‌خورد.
        """
        payload = {
            'username': 'nonexistentuser',
            'password': self.password
        }
        response = self.client.post(self.login_url, payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_without_password_fails(self):
        """
        تست می‌کند که عدم ارسال فیلد رمز عبور، با کد 400 Bad Request شکست می‌خورد.
        """
        payload = {
            'username': self.username,
        }
        response = self.client.post(self.login_url, payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        self.assertIn('password', response.data)