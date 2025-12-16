
from rest_framework import serializers
from .models import Profile

class StudentUnitLimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['min_units', 'max_units']

    def validate(self, data):
        min_u = data.get('min_units')
        max_u = data.get('max_units')

        if min_u > max_u:
            raise serializers.ValidationError(
                "minimum unit can't be higher than maximum units"
            )

        return data
