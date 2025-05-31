from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from django.shortcuts import redirect
from django.core.serializers import serialize
from django.shortcuts import render

from .models import Task
from .serializers import TaskSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = []
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "pages/index.html"

    def get(self, request):
        if request.user.is_authenticated:
            # Пользователь залогинен: показываем все его задачи (и приватные, и нет)
            tasks = Task.objects.filter(user=request.user)
        else:
            # Не залогинен: показываем только публичные задачи
            tasks = Task.objects.filter(is_private=False)

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return redirect('task-list-create')
        tasks = Task.objects.filter(user=request.user)
        return Response({'tasks': tasks, 'form': serializer})


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "pages/task_detail.html"

    def get(self, request):
        if request.user.is_authenticated:
            # Пользователь залогинен: показываем все его задачи (и приватные, и нет)
            tasks = Task.objects.filter(user=request.user)
        else:
            # Не залогинен: показываем только публичные задачи
            tasks = Task.objects.filter(is_private=False)

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        if "delete" in request.POST:
            task.delete()
            return redirect("task-list-create")
        serializer = self.get_serializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect("task-list-create")
        return Response({'task': task, 'form': serializer})
