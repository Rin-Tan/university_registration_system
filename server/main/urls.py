from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # path('', views.student_unit_management, name='student-unit-management'),
    
]