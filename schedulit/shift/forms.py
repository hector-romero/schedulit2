from django import forms
from django.utils.translation import gettext_lazy as _

from schedulit.shift.models import Shift, ShiftNote


class ShiftForm(forms.ModelForm[Shift]):
    def clean(self):
        super().clean()
        cleaned_data = self.cleaned_data
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if not start_time or not end_time or start_time >= end_time:
            raise forms.ValidationError(_("Start time should be earlier than end time."))
        return self.cleaned_data

    class Meta:
        fields = ['start_time', 'end_time', 'employee']
        model = Shift


class ShiftNoteForm(forms.ModelForm[ShiftNote]):
    class Meta:
        fields = ['note', 'shift']
        model = ShiftNote
