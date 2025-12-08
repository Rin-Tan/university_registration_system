from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'course_code', 'capacity', 'units','day_of_week','location','start_time','end_time','prerequisites' ]
    
    def validate(self, data):
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        capacity = data.get("capacity")
        units = data.get("units")
        course_code = data.get("course_code")

        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError(
                {"time": "Start time must be earlier than end time."}
            )

        if capacity is not None and capacity <= 0:
            raise serializers.ValidationError(
                {"capacity": "Capacity must be greater than 0."}
            )

        if units is not None and not (1 <= units <= 5):
            raise serializers.ValidationError(
                {"units": "Units must be between 1 and 5."}
            )

        return data

    def validate_course_code(self, value):

        qs = Course.objects.filter(course_code=value)

    
        if self.instance:
            qs = qs.exclude(id=self.instance.id)

        if qs.exists():
            raise serializers.ValidationError("Course code must be unique.")

        return value

    