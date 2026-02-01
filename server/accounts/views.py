import requests
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.views import View
from django.http import HttpResponse
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.models import Profile
from courses.models import Course
from .serializers import StudentUnitLimitSerializer


class UpdateStudentUnitLimitAPIView(generics.UpdateAPIView):
    queryset = Profile.objects.filter(role='student')
    serializer_class = StudentUnitLimitSerializer


def verify_captcha(captcha_token):
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
    def post(self, request, *args, **kwargs):
        captcha_response = request.data.get("g-recaptcha-response")

        if not captcha_response or not verify_captcha(captcha_response):
            return Response(
                {"error": "invalid-captcha"},
                status=status.HTTP_400_BAD_REQUEST
            )

        response = super().post(request, *args, **kwargs)

        if response.status_code != 200:
            return response

        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is None:
            return response

        login(request, user)

        try:
            profile = user.profile
        except Profile.DoesNotExist:
            return response

        if profile.is_student():
            redirect_url = "/student/mycourses"
        elif profile.is_teacher():
            redirect_url = "/professor_courses/"
        elif profile.is_manager():
            redirect_url = "/courses/"
        else:
            redirect_url = "/"

        data = response.data
        data["redirect"] = redirect_url
        data["role"] = profile.role

        return Response(data, status=status.HTTP_200_OK)


class LoginRenderView(View):
    def get(self, request):
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("/")


@login_required
def dashboard_view(request):
    user = request.user

    try:
        profile = user.profile
    except Profile.DoesNotExist:
        logout(request)
        return redirect("/")

    if profile.is_manager():
        return redirect("/courses/")

    if profile.is_teacher():
        return redirect("/professor_courses/")

    if profile.is_student():
        return redirect("/student/mycourses")

    logout(request)
    return redirect("/")


@login_required
def add_course_view(request):
    if not request.user.profile.is_manager():
        return HttpResponse("Forbidden", status=403)
    return render(request, "dashboard.html")


@login_required
def delete_course_view(request, course_id):
    if not request.user.profile.is_manager():
        return HttpResponse("Forbidden", status=403)

    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return redirect("/courses/")


class CustomLogoutAPIView(APIView):
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
