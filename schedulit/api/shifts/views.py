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
        queryset = Shift.objects.all()
        if 'employee_id' in self.kwargs:
            queryset = queryset.filter(employee_id=self.kwargs['employee_id'])
        return queryset

    def create(self, request: Request, *args: typing.Any, **kwargs: typing.Any) -> Response:
        request.data['employee_id'] = kwargs['employee_id']
        request.data['employee'] = kwargs['employee_id']
        return super().create(request, *args, **kwargs)
