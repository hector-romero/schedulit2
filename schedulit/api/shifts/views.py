import typing

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from schedulit.api.shifts.serializers import ShiftSerializer
from schedulit.api.utils import BaseSchedulerView
from schedulit.shift.models import Shift


class ShiftView(ModelViewSet, BaseSchedulerView):
    serializer_class = ShiftSerializer

    def get_queryset(self):
        employee_id = self.kwargs['employee_id']
        return Shift.objects.filter(employee_id=employee_id)

    def create(self, request: Request, *args: typing.Any, **kwargs: typing.Any) -> Response:
        request.data['employee'] = kwargs['employee_id']
        return super().create(request, *args, **kwargs)
