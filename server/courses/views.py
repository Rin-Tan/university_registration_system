from django.shortcuts import render
from .models import Course
from rest_framework import generics
from .serializers import CourseSerializer


class CourseListCreate(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = "pk"

def courses_page(request):
    return render(request, "courses.html")
