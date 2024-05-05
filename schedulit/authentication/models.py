from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import UniqueConstraint, Q
from django.db.models.functions import Lower
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from schedulit.authentication.managers import UserManager
from schedulit.utils.models import TextChoices


# Using a custom user instead of the standard Django User because I want the freedom of adjusting it to my needs
# For a start, there were several fields I didn't need (username, first-last name) and I also wanted to add role and
# employee_id to avoid having to add an extra model to store that data.
class User(AbstractBaseUser, PermissionsMixin):
    class Roles(TextChoices):
        SCHEDULER = 'scheduler'
        EMPLOYEE = 'employee'

    name = models.CharField(_("Name"), max_length=150, blank=True, default='')
    role = Roles.model_field(default=Roles.EMPLOYEE)
    employee_id = models.CharField(verbose_name='Employee ID', max_length=50, default='', blank=True, null=False)

    # Not interested in having username and email, using email for login
    email = models.EmailField(_("email address"), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role', 'employee_id']

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    class Meta:
        # noinspection PyArgumentList
        constraints = [
            # Makes sure that email uniqueness is case-insensitive
            UniqueConstraint(Lower('email'), name='unique_email',
                             violation_error_message=_('user with this email address already exists.')),
            # Employee id is not required (can be an empty string), but makes sure that, when defined, it's unique
            UniqueConstraint('employee_id', condition=Q(employee_id__gt=''), name='unique_employee_id',
                             violation_error_message=_('Employee ID already in use.'))
        ]

    def _is_role(self, role: Roles) -> bool:
        return self.role == role.value

    @property
    def is_employee(self) -> bool:
        # Assuming employee role is the default (in case there's no role in the user for some reason)
        return not self.role or self._is_role(User.Roles.EMPLOYEE)

    @property
    def is_scheduler(self) -> bool:
        return self._is_role(User.Roles.SCHEDULER)
