import typing

import rest_framework.exceptions
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from schedulit.api.shifts.serializers import ShiftSerializer
from schedulit.api.utils import BaseSchedulerView
from schedulit.authentication.models import User
from schedulit.shift.models import Shift


class ShiftView(ModelViewSet[Shift], BaseSchedulerView):
    serializer_class = ShiftSerializer
    parser_classes = [JSONParser]

    def get_queryset(self):
        queryset = Shift.objects.all()
        if 'employee_id' in self.kwargs:
            # Raise 404 if the user indicated does not exist
            # try:
            #     employee = User.objects.get(id=self.kwargs['employee_id'])
            # except User.DoesNotExist as e:
            #     raise rest_framework.exceptions.NotFound from e
            queryset = queryset.filter(employee=self.kwargs['employee_id'])
        return queryset

    def get_employee(self) -> User:
        try:
            return User.objects.get(id=self.kwargs['employee_id'])
        except (User.DoesNotExist, KeyError) as e:
            raise rest_framework.exceptions.NotFound from e

    def create(self, request: Request, *args: typing.Any, **kwargs: typing.Any) -> Response:
        try:
            request.data['employee'] = self.get_employee().id
        except TypeError:
            # This is in for when the input data is not a dict. In that case I don't really care
            # about setting employee_id, the creation will fail anyway
            pass
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        # Queries employee to validate it
        self.get_employee()
        return super().list(request, *args, **kwargs)
