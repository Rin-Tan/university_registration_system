from django.shortcuts import render
from .models import Course
from rest_framework import generics
from .serializers import CourseSerializer

# -------------------  Course API   -------------------
class CourseListCreate(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    # permission_classes = [permissions.IsAdminUser]

class CourseRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    # permission_classes = [permissions.IsAdminUser]


# -------------------  TimeSlot API   -------------------

from rest_framework import generics
from .models import TimeSlot
from .serializers import TimeSlotSerializer

class TimeSlotListCreate(generics.ListCreateAPIView):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer


class TimeSlotRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer


def courses_page(request):
    return render(request, "courses.html")
