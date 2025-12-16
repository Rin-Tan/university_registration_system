from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.courses_page, name='courses_page'),
    
    path('api/v1/courses/', views.CourseListCreate.as_view(), name="course-view-create"),
    path('api/v1/courses/<int:pk>/', views.CourseRetrieveUpdateDestroy.as_view(), name="course-update-destroy"),
    
    path('api/v1/timeslots/', views.TimeSlotListCreate.as_view(), name='timeslot-list-create'),
    path('api/v1/timeslots/<int:pk>/', views.TimeSlotRetrieveUpdateDestroy.as_view(), name='timeslot-rud'),
   
]
