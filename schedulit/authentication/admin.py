from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from schedulit.authentication.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['employee_id', 'email', 'full_name', 'role', 'date_joined', 'last_login']
    # list_filter = ['is_staff', 'is_superuser', 'date_joined', 'groups']
    fieldsets = [
        (None, {'fields': ['email', 'name', 'role', 'employee_id']}),

        ('Permissions', {'fields': ['is_staff', 'is_superuser']}),
        (None, {'fields': ['date_joined', 'last_login', 'password']}),
    ]
    readonly_fields = ['date_joined', 'last_login']

    add_fieldsets = [
        (None, {
            "classes": ['wide'],
            "fields": ['email', 'name', 'employee_id', 'role', 'password1', 'password2'],
        })
    ]
    search_fields = ['email', 'name', 'role']
    ordering = ['role', 'email']
    list_display_links = ['email', 'employee_id']

    @staticmethod
    def full_name(user):
        return user.name or 'N/A'
