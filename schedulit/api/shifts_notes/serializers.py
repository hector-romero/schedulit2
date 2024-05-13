from rest_framework import serializers

from schedulit.shift.models import ShiftNote


class ShiftNoteSerializer(serializers.ModelSerializer[ShiftNote]):
    class Meta:
        model = ShiftNote
        fields = ['id', 'timestamp', 'note', 'shift', 'shift_id']
        extra_kwargs = {
            'shift': {'required': True, 'write_only': True},
            'timestamp': {'read_only': True}
        }
