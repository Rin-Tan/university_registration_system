from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
            model = Course
            fields = ['id', 'title', 'course_code', 'capacity', 'units','day_of_week','location','start_time','end_time','prerequisites' ]
