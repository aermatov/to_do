from django.shortcuts import render

from tasks.models import Task


def get_index(request):
    gigi = "Nazgul"
    tasks = Task.objects.all()
    return render(request, "index.html", locals())
