from typing import TYPE_CHECKING

from django.contrib.auth.models import BaseUserManager as DjangoUserManager
from django.db.models import Q

if TYPE_CHECKING:
    from schedulit.authentication.models import User


class UserManager(DjangoUserManager['User']):
    def _create_user(self, email: str = None, name: str = None, password: str = None,
                     employee_id: str = None, role: 'User.Roles' = None,
                     is_staff: bool = False, is_superuser: bool = False) -> 'User':
        user = self.model(
            email=self.normalize_email(email),
            name=str(name or '').strip(),
            role=role or self.model.Roles.EMPLOYEE,
            employee_id=str(employee_id or '').strip(),
            is_staff=is_superuser or is_staff,
            is_superuser=is_superuser
        )
        user.set_password(password)
        return user

    def create_user(self, email: str = None, name: str = None, password: str = None,
                    employee_id: str = None, role: 'User.Roles' = None,
                    is_staff: bool = False, is_superuser: bool = False) -> 'User':
        """
        Creates and saves a User with the given email, phone and password.
        """
        user = self._create_user(email=email, name=name, password=password,
                                 employee_id=employee_id, role=role, is_staff=is_staff, is_superuser=is_superuser)
        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str = None, name: str = None, password: str = None,
                         employee_id: str = None, role: 'User.Roles' = None) -> 'User':
        user = self.create_user(email=email, name=name, password=password,
                                employee_id=employee_id, role=role, is_staff=True, is_superuser=True)
        return user

    # Allow user login by email, case-insensitive
    def get_by_natural_key(self, username: str | None) -> 'User':
        username = str(username).lower().strip()
        return self.get(Q(email__iexact=username))
