from django.contrib import admin
from advanced_func.models import Overdue


class OverdueAdmin(admin.ModelAdmin):
    list_display = ['id', 'task', 'due_date']

admin.site.register(Overdue, OverdueAdmin)