from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from django.shortcuts import redirect
from django.core.serializers import serialize
from django.shortcuts import render
from django.contrib import messages

from .forms import TaskForm
from .models import Task
from .serializers import TaskSerializer


def index(request):
    return render(request, 'pages/index.html')


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

    def task_create(request):
        if request.method == 'POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.save()
                messages.success(request, 'Задача успешно создана!')
                return redirect('task-list-create')
            else:
                messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
        else:
            form = TaskForm()

        return render(request, 'pages/index.html', {
            'form': form,
            'tasks': Task.objects.filter(user=request.user)
        })


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


from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'index.html'  # Указываем ваш существующий шаблон

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        if self.request.user.is_authenticated:
            context['user'] = self.request.user
        return context
