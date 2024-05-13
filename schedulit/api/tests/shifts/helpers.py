import typing
from datetime import datetime

from model_bakery import baker, random_gen

from schedulit.authentication.models import User
from schedulit.shift.models import Shift

ShiftParams = typing.TypedDict('ShiftParams', {
    'start_time': datetime, 'end_time': datetime}, total=False)


def get_shift_params(shift: Shift) -> ShiftParams:
    return ShiftParams(start_time=shift.start_time, end_time=shift.end_time)


def generate_shift_params() -> ShiftParams:
    date_range = random_gen.gen_datetime_range()  # type: ignore[no-untyped-call]
    return ShiftParams(start_time=date_range.lower, end_time=date_range.upper)


def prepare_shift(employee: User) -> Shift:
    params = generate_shift_params()
    return baker.prepare(Shift, start_time=params['start_time'], end_time=params['end_time'], employee=employee)
