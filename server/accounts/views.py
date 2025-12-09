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