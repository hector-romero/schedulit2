from django.db import models

from django.utils.translation import gettext_lazy as _

from schedulit.authentication.models import User
from schedulit.utils.models import TextChoices, TimestampedModel


class Shift(TimestampedModel):
    class Statuses(TextChoices):
        CREATED = 'created'
        ACCEPTED = 'accepted'
        COMPLETED = 'completed'
        REJECTED = 'rejected'

    start_time = models.DateTimeField(_('Start time'), null=False, blank=False)
    end_time = models.DateTimeField(_('End time'), null=False, blank=False)
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shifts', null=False)
    status = Statuses.model_field(_('Status'), default=Statuses.CREATED)

    def __str__(self):
        def _format_datetime(date):
            return date.strftime('%Y-%m-%d %H:%M:%S')
        return f"{_format_datetime(self.start_time)} to {_format_datetime(self.end_time)}"

    class Meta:
        default_related_name = 'shifts'
        ordering = ['start_time']


class ShiftNote(TimestampedModel):
    note = models.CharField(_('Note'), max_length=50, blank=False, null=False)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='notes', null=False)

    def __str__(self) -> str:
        return self.note
