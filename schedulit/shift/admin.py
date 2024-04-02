from django.contrib import admin

from schedulit.authentication.models import User
from schedulit.shift.models import Shift, ShiftNote


class ShiftNoteInline(admin.TabularInline):
    fields = ('timestamp', 'note')
    readonly_fields = ('timestamp',)
    model = ShiftNote
    extra = 0

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Shift)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_time', 'end_time', 'status')
    inlines = [ShiftNoteInline]

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj=None, change=False, **kwargs)
        form.base_fields['employee'].queryset = User.objects.filter(role=User.Roles.EMPLOYEE)
        return form
