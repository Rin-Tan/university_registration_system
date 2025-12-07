"""
URL configuration for University_Registoration_Sys project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    # TokenBlacklistView دیگر مستقیماً در اینجا استفاده نمی‌شود
)
from accounts.views import CustomLogoutView # View سفارشی که در مرحله ۲ می‌نویسیم

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('courses.urls')),



    # 1. ورود (POST /api/sessions/): ایجاد منبع نشست
    path('api/sessions/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # 2. تمدید (POST /api/sessions/refresh/): به‌روزرسانی منبع نشست
    path('api/sessions/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 3. خروج (DELETE /api/sessions/current/): حذف منبع نشست
    # ما از CustomLogoutView استفاده می‌کنیم تا بتوانیم متد DELETE را بپذیریم.
    path('api/sessions/current/', CustomLogoutView.as_view(), name='logout'),

]
