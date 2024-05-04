from datetime import datetime, timedelta

from django.test import TestCase
from django.utils import timezone
from model_bakery import baker

from schedulit.authentication.models import User
from schedulit.shift.forms import ShiftForm, ShiftNoteForm
from schedulit.shift.models import Shift, ShiftNote


class ShiftTest(TestCase):
    employee: User
    now: datetime
    now_minus_2hs: datetime
    now_plus_2hs: datetime

    @classmethod
    def setUpTestData(cls):
        cls.employee = baker.make(User, role=User.Roles.EMPLOYEE)

        now = datetime.now()
        now_minus_2hs = now - timedelta(hours=2)
        now_plus_2hs = now + timedelta(hours=2)

        cls.now = timezone.make_aware(now)
        cls.now_minus_2hs = timezone.make_aware(now_minus_2hs)
        cls.now_plus_2hs = timezone.make_aware(now_plus_2hs)

    @staticmethod
    def create_shift(start_time: datetime | None, end_time: datetime | None, employee: User | None) -> Shift:
        form = ShiftForm(data={
            'start_time': start_time,
            'end_time': end_time,
            'employee': employee
        })

        return form.save()

    def test_should_create_shift(self):
        shift = self.create_shift(start_time=self.now, end_time=self.now_plus_2hs, employee=self.employee)
        self.assertIsNotNone(shift)
        self.assertEqual(shift.start_time, self.now)
        self.assertEqual(shift.end_time, self.now_plus_2hs)
        self.assertEqual(shift.employee_id, self.employee.id)
        self.assertEqual(shift.status, Shift.Statuses.CREATED)

    def test_should_not_allow_creating_shift_with_invalid_start_time(self):
        self.assertRaises(ValueError, self.create_shift,
                          start_time=None, end_time=self.now_plus_2hs, employee=self.employee)
        self.assertRaises(ValueError, self.create_shift,
                          start_time="a string", end_time=self.now_plus_2hs, employee=self.employee)
        # The following should raise a value error, but instead it raises AttributeError because django executes
        # to value.strip() assuming the value for this field is going to be a string (or other type with .strip())
        # and only catches the ValueError instead of other exceptions.
        # https://github.com/django/django/blob/5f180216409d75290478c71ddb0ff8a68c91dc16/django/forms/fields.py#L550
        self.assertRaises(AttributeError, self.create_shift,
                          start_time=1234, end_time=self.now_plus_2hs, employee=self.employee)
        # Only a time:
        self.assertRaises(AttributeError, self.create_shift,
                          start_time=datetime.now().time(), end_time=self.now_plus_2hs, employee=self.employee)

    def test_should_not_allow_creating_shift_without_end_time(self):
        self.assertRaises(ValueError, self.create_shift,
                          start_time=self.now, end_time=None, employee=self.employee)
        self.assertRaises(ValueError, self.create_shift,
                          start_time=self.now, end_time="a string", employee=self.employee)
        # The following should raise a value error, but instead it raises AttributeError because django executes
        # to value.strip() assuming the value for this field is going to be a string (or other type with .strip())
        # and only catches the ValueError instead of other exceptions.
        # https://github.com/django/django/blob/5f180216409d75290478c71ddb0ff8a68c91dc16/django/forms/fields.py#L550
        self.assertRaises(AttributeError, self.create_shift,
                          start_time=self.now, end_time=1234, employee=self.employee)
        # Only a time:
        self.assertRaises(AttributeError, self.create_shift,
                          start_time=self.now_minus_2hs, end_time=self.now.time(), employee=self.employee)

    def test_should_not_allow_creating_shift_with_invalid_employee(self):
        self.assertRaises(ValueError, self.create_shift,
                          start_time=self.now, end_time=self.now_plus_2hs, employee=None)
        self.assertRaises(ValueError, self.create_shift,
                          start_time=self.now, end_time=self.now_plus_2hs, employee="a string")
        self.assertRaises(ValueError, self.create_shift,
                          start_time=self.now, end_time=self.now_plus_2hs, employee=1234)
        # A non saved user
        self.assertRaises(ValueError, self.create_shift,
                          start_time=self.now, end_time=self.now_plus_2hs, employee=User())

    def test_should_not_allow_creating_shift_with_earlier_end_time_than_start_time(self):
        self.assertRaises(ValueError, self.create_shift,
                          start_time=self.now, end_time=self.now_minus_2hs, employee=self.employee)


class ShiftNoteTest(TestCase):
    shift: Shift

    @classmethod
    def setUpTestData(cls):
        cls.shift = baker.make(Shift)

    @staticmethod
    def create_shift_note(note: str | None, shift: Shift | None) -> ShiftNote:
        form = ShiftNoteForm(data={
            'shift': shift,
            'note': note
        })
        return form.save()

    def test_should_create_shift_note(self):
        note = "some note"
        shift_note = self.create_shift_note(note=note, shift=self.shift)
        self.assertIsNotNone(shift_note)
        self.assertEqual(shift_note.note, note)
        self.assertEqual(shift_note.shift_id, self.shift.id)

    def test_should_not_allow_to_create_shift_note_with_invalid_note(self):
        self.assertRaises(ValueError, self.create_shift_note, note=None, shift=self.shift)
        self.assertRaises(ValueError, self.create_shift_note, note='', shift=self.shift)

    def test_should_not_allow_to_create_shift_note_with_invalid_shift(self):
        self.assertRaises(ValueError, self.create_shift_note, note="note", shift=None)
        self.assertRaises(ValueError, self.create_shift_note, note="note", shift="some string")
        self.assertRaises(ValueError, self.create_shift_note, note="note", shift=1234)
        self.assertRaises(ValueError, self.create_shift_note, note="note", shift=Shift())
