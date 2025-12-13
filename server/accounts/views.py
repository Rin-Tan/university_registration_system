import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

def verify_captcha(captcha_token):
    """
    این تابع توکن کپچا را به گوگل می‌فرستد تا تایید کند که کاربر ربات نیست.
    """
    if not captcha_token:
        return False
        
    url = "https://www.google.com/recaptcha/api/siteverify"
    data = {
        "secret": settings.RECAPTCHA_SECRET_KEY,
        "response": captcha_token,
    }
    
    try:
        response = requests.post(url, data=data)
        result = response.json()
        return result.get("success", False)
    except Exception:
        return False

class CustomLoginView(TokenObtainPairView):
    """
    این کلاس جایگزین لاگین پیش‌فرض می‌شود.
    ابتدا کپچا را چک می‌کند، اگر درست بود، توکن JWT می‌دهد.
    """
    def post(self, request, *args, **kwargs):
        captcha_response = request.data.get("g-recaptcha-response")

        if not captcha_response:
            return Response(
                {"error": "captcha-required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if not verify_captcha(captcha_response):
            return Response(
                {"error": "invalid-captcha"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().post(request, *args, **kwargs)


class CustomLogoutView(APIView):
    """
    پیاده‌سازی اندپوینت خروج: DELETE /api/sessions/current/
    این View توکن Refresh ارسال شده را در لیست سیاه (Blacklist) قرار می‌دهد.
    """
    
    permission_classes = (IsAuthenticated,) 

    def delete(self, request):
        """
        هندل کردن درخواست DELETE برای حذف منبع نشست.
        """
        refresh_token = request.data.get("refresh") 
        
        if not refresh_token:
            return Response(
                {"detail": "Refresh token is required to delete the session."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            token = RefreshToken(refresh_token)
            token.blacklist() 
            return Response(status=status.HTTP_204_NO_CONTENT) 
            
        except Exception as e:
            return Response(
                {"detail": "Token is invalid or already blacklisted."}, 
                status=status.HTTP_400_BAD_REQUEST
            )