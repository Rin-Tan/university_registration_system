# accounts/views.py

import requests
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views import View 
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login 
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Profile
from .serializers import StudentUnitLimitSerializer

from accounts.models import Profile 
from courses.models import Course 


class UpdateStudentUnitLimitAPIView(generics.UpdateAPIView):
    queryset = Profile.objects.filter(role='student')
    serializer_class = StudentUnitLimitSerializer



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

# accounts/views.py

class CustomLoginView(TokenObtainPairView):
    """
    این کلاس جایگزین لاگین پیش‌فرض می‌شود.
    JWT صادر می‌کند و سپس Session را ایجاد می‌کند. 🌟
    """
    def post(self, request, *args, **kwargs):
        captcha_response = request.data.get("g-recaptcha-response")

        if not captcha_response or not verify_captcha(captcha_response):
            return Response(
                {"error": "invalid-captcha"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 1. اجرای منطق اصلی JWT (صدور توکن)
        response = super().post(request, *args, **kwargs)

        # 2. اگر لاگین JWT موفق بود، کاربر را وارد Session کنید
        if response.status_code == 200:
            username = request.data.get("username")
            password = request.data.get("password")
            
            # احراز هویت کاربر برای دریافت آبجکت User
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # 🌟🌟 ایجاد Session برای کاربر (این قسمت ضروری است) 🌟🌟
                login(request, user)
                
                # شما می‌توانید یک پیام موفقیت آمیز Session نیز ارسال کنید (اختیاری)
                # from django.contrib import messages
                # messages.success(request, f"Welcome back, {user.username}!")
                
            else:
                # اگرچه JWT موفق بوده، اما احراز هویت Session شکست خورده است (نباید رخ دهد)
                # اما ما Session را ایجاد نکردیم، فقط JWT را برگرداندیم.
                pass # لاگین Session در این حالت شکست نمی‌خورد، فقط Session ایجاد نمی‌شود.

        return response # پاسخی که شامل توکن JWT است را برمی‌گردانیم.



class LoginRenderView(View):
    def get(self, request):
        return render(request, 'login.html')


def logout_view(request):
    """
    #  تابع لاگ‌اوت تمام داده‌های سشن کاربر فعلی را پاک کرده و کاربر را ناشناس می‌کند.
    """
    logout(request)
    return redirect('login') 



@login_required(login_url='/login/') 
def dashboard_view(request):
    
    user = request.user
    context = {}
    
    try:
        profile = user.profile 
    except Profile.DoesNotExist:
        logout(request) 
        return redirect('login') 
        
    courses = Course.objects.none()

    if profile.is_manager():
        courses = Course.objects.all()
        context['can_manage_courses'] = True 
        context['user_role'] = 'manager'
        template_name = 'dashboard.html'
        
    elif profile.is_teacher():
        courses = Course.objects.filter(professor=profile) 
        context['can_manage_courses'] = False
        context['user_role'] = 'teacher'
        template_name = 'dashboard_teacher.html'
        
    elif profile.is_student():
        courses = Course.objects.filter(students=profile)
        context['can_manage_courses'] = False
        context['user_role'] = 'student'
        template_name = 'student-unit-management.html' 
        
    else:
        logout(request)
        return redirect('login')

    context['courses'] = courses
    return render(request, template_name, context)


@login_required(login_url='/login/')
def add_course_view(request):
    if not request.user.profile.is_manager():
        return HttpResponse("شما اجازه اضافه کردن درس را ندارید.", status=403)
    
    #  اینجا میتونیم منطق اضافه کردن درس جدید را پیاده‌سازی کنیم.
    
    return render(request, 'dashboard.html') 

@login_required(login_url='/login/')
def delete_course_view(request, course_id):

    if not request.user.profile.is_manager():
        return HttpResponse("شما اجازه حذف درس را ندارید.", status=403)

    course = get_object_or_404(Course, id=course_id)
    course.delete()
    
    return redirect('dashboard')



class CustomLogoutAPIView(APIView):
    """
    پیاده‌سازی اندپوینت خروج API: توکن Refresh ارسال شده را در لیست سیاه قرار می‌دهد.
    """
    permission_classes = (IsAuthenticated,) 

    def delete(self, request):
        refresh_token = request.data.get("refresh") 
        
        if not refresh_token:
            return Response(
                {"detail": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            token = RefreshToken(refresh_token)
            token.blacklist() 
            return Response(status=status.HTTP_204_NO_CONTENT) 
            
        except Exception:
            return Response(
                {"detail": "Token is invalid or already blacklisted."}, 
                status=status.HTTP_400_BAD_REQUEST
            )