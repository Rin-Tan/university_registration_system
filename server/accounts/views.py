from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

class CustomLogoutView(APIView):
    """
    پیاده‌سازی اندپوینت خروج: DELETE /api/sessions/current/
    این View توکن Refresh ارسال شده را در لیست سیاه (Blacklist) قرار می‌دهد.
    """
    
    # اطمینان حاصل می‌کند که فقط کاربرانی که لاگین کرده‌اند بتوانند توکن خود را باطل کنند.
    permission_classes = (IsAuthenticated,) 

    def delete(self, request):
        """
        هندل کردن درخواست DELETE برای حذف منبع نشست.
        """
        # توکن Refresh باید در بدنه (Payload) با کلید 'refresh' ارسال شود.
        refresh_token = request.data.get("refresh") 
        
        # ۱. بررسی وجود توکن
        if not refresh_token:
            return Response(
                {"detail": "Refresh token is required to delete the session."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            # ۲. ایجاد شیء RefreshToken
            token = RefreshToken(refresh_token)
            
            # ۳. ابطال توکن (عملیات حذف منبع)
            # این خط توکن را در دیتابیس در لیست سیاه قرار می‌دهد.
            token.blacklist() 
            
            # ۴. بازگشت کد وضعیت موفقیت‌آمیز
            # 204 No Content کد استاندارد برای عملیات DELETE موفق است.
            return Response(status=status.HTTP_204_NO_CONTENT) 
            
        except Exception as e:
            # ۵. بازگشت کد وضعیت خطا
            # اگر توکن نامعتبر یا از قبل باطل شده باشد.
            return Response(
                {"detail": "Token is invalid or already blacklisted."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

# توجه: این View باید در urls.py به مسیر 'api/sessions/current/' با متد DELETE متصل شود.