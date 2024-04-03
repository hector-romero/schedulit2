from rest_framework.viewsets import ReadOnlyModelViewSet

from schedulit.api.shifts.serializers import ShiftSerializer
from schedulit.api.utils import BaseSchedulerView
from schedulit.shift.models import Shift


class ShiftView(ReadOnlyModelViewSet, BaseSchedulerView):
    serializer_class = ShiftSerializer

    def get_queryset(self):
        employee_id = self.kwargs['employee_id']
        return Shift.objects.filter(employee_id=employee_id)
