from django.contrib import admin
from django.urls import path, include
# import‌های اضافه شده توسط دوستتان
from courses import views 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    # TokenBlacklistView دیگر مستقیماً در اینجا استفاده نمی‌شود
)
from accounts.views import CustomLogoutView # View سفارشی که در مرحله ۲ می‌نویسیم

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # مسیر دوستتان برای دسترسی به دوره‌ها
    path('courses/', include('courses.urls')), 
    
    # مسیر دوستتان برای دسترسی به داشبورد
    path('dashboard/', include('main.urls')),
    
    # مسیر قدیمی شما که احتمالا دیگر لازم نیست اما برای اطمینان نگه می‌داریم
    # اگر پروژه شما به آن نیاز ندارد می‌توانید حذف کنید، اما فعلا نگه می‌داریم
    # path('',include('courses.urls')), 
    
    
    # 1. ورود (POST /api/sessions/): ایجاد منبع نشست
    path('api/sessions/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # 2. تمدید (POST /api/sessions/refresh/): به‌روزرسانی منبع نشست
    path('api/sessions/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 3. خروج (DELETE /api/sessions/current/): حذف منبع نشست
    # ما از CustomLogoutView استفاده می‌کنیم تا بتوانیم متد DELETE را بپذیریم.
    path('api/sessions/current/', CustomLogoutView.as_view(), name='logout'),

]