
from django.urls import path
from .views import UpdateStudentUnitLimitAPIView

urlpatterns = [
    path(
        'students/<int:pk>/unit-limits/',
        UpdateStudentUnitLimitAPIView.as_view(),
        name='student-unit-limits'
    ),
]
