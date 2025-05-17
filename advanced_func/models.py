from django.db import models

from tasks.models import Task


class Overdue(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='advanced_func')
    due_date = models.DateTimeField()
