from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # path('', views.index, name ='index'),
    path('courses/', views.CourseListCreate.as_view(), name="course-view-create"),
    path('courses/<int:pk>/', views.CourseRetrieveUpdateDestroy.as_view(), name="course-update"),
]
