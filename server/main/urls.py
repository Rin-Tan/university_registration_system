from django.urls import path
from .views import professor_courses
urlpatterns = [
    path('',professor_courses, name='professor_courses'),
]