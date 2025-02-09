from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from schedulit.shift.models import Shift


class ShiftSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        start_time = attrs.get('start_time')
        end_time = attrs.get('end_time')
        # TODO Check overlapping with other shifts
        if not start_time or not end_time or start_time >= end_time:
            raise serializers.ValidationError(_("End time should be greater than start time."))
        return attrs

    class Meta:
        model = Shift
        fields = ['id', 'timestamp', 'start_time', 'end_time', 'status', 'employee_id', 'employee']
        extra_kwargs = {
            'employee': {'required': True, 'write_only': True},
            'timestamp': {'read_only': True}
        }
