from django.contrib import admin
from tasks.models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'is_completed']
    readonly_fields = ['created_at',]


admin.site.register(Task, TaskAdmin)