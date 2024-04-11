import typing

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from schedulit.api.shifts_notes.serializers import ShiftNoteSerializer
from schedulit.api.utils import BaseSchedulerView
from schedulit.shift.models import ShiftNote


class ShiftNotesView(ModelViewSet, BaseSchedulerView):
    serializer_class = ShiftNoteSerializer

    def get_queryset(self):
        queryset = ShiftNote.objects.all()
        if 'shift_id' in self.kwargs:
            queryset = queryset.filter(shift_id=self.kwargs['shift_id'])
        return queryset

    def create(self, request: Request, *args: typing.Any, **kwargs: typing.Any) -> Response:
        request.data['shift'] = kwargs['shift_id']
        return super().create(request, *args, **kwargs)
