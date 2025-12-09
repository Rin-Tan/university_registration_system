from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from django.urls import reverse

class LoginAPITests(APITestCase):
    
    # متد راه‌اندازی: قبل از هر تست اجرا می‌شود
    def setUp(self):
        # ساخت یک کاربر تست برای استفاده در تمام تست‌ها
        self.username = 'testuser'
        self.password = 'StrongPass123'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )
        # آدرس API لاگین (همان 'api/sessions/')
        self.login_url = reverse('token_obtain_pair')
        
        # داده‌های صحیح لاگین
        self.valid_payload = {
            'username': self.username,
            'password': self.password
        }
        
        # داده‌های اشتباه لاگین
        self.invalid_payload = {
            'username': self.username,
            'password': 'wrongpassword'
        }

    # 1. تست لاگین موفق (دریافت توکن)
    def test_successful_login_returns_tokens(self):
        """
        تست می‌کند که لاگین با اعتبارنامه صحیح، کد 200 و توکن‌های access/refresh را برمی‌گرداند.
        """
        response = self.client.post(self.login_url, self.valid_payload, format='json')
        
        # بررسی کد وضعیت (Status Code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # بررسی محتوای پاسخ (حتما باید توکن‌ها را برگرداند)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    # 2. تست شکست لاگین با رمز عبور اشتباه
    def test_login_with_incorrect_password_fails(self):
        """
        تست می‌کند که لاگین با رمز عبور اشتباه، با کد 401 Unauthorized شکست می‌خورد.
        """
        response = self.client.post(self.login_url, self.invalid_payload, format='json')
        
        # بررسی کد وضعیت (باید 401 باشد)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # بررسی که نباید توکن برگرداند
        self.assertNotIn('access', response.data)

    # 3. تست شکست لاگین با نام کاربری ناموجود
    def test_login_with_nonexistent_user_fails(self):
        """
        تست می‌کند که اگر نام کاربری وجود نداشته باشد، لاگین شکست می‌خورد.
        """
        payload = {
            'username': 'nonexistentuser',
            'password': self.password
        }
        response = self.client.post(self.login_url, payload, format='json')
        
        # بررسی کد وضعیت (باید 401 باشد)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # 4. تست عدم ارسال رمز عبور (Validation Error)
    def test_login_without_password_fails(self):
        """
        تست می‌کند که عدم ارسال فیلد رمز عبور، با کد 400 Bad Request شکست می‌خورد.
        """
        payload = {
            'username': self.username,
            # 'password': 'رمز عبور ارسال نشده'
        }
        response = self.client.post(self.login_url, payload, format='json')
        
        # بررسی کد وضعیت (باید 400 باشد چون فیلد الزامی کم است)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # بررسی که پیام خطا در پاسخ وجود داشته باشد
        self.assertIn('password', response.data)