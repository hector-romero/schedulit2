import typing

from schedulit.authentication.models import User

UserParams = typing.TypedDict('UserParams', {
    'email': str, 'password': 'str', 'name': 'str', 'role': User.Roles | str, 'employee_id': str | None
}, total=False)


def get_user_params(user: User) -> UserParams:
    return UserParams(
        email=user.email, password=user.password, name=user.name, role=user.role, employee_id=user.employee_id)
