from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.courses_page, name='courses_page'),
    path('api/V1/courses/', views.CourseListCreate.as_view(), name="course-view-create"),
    path('api/V1/courses/<int:pk>/', views.CourseRetrieveUpdateDestroy.as_view(), name="course-update-destroy"),
    
]
