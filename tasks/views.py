from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from django.shortcuts import redirect, render
from django.core.serializers import serialize
from django.contrib import messages
from django.views.generic import TemplateView

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
        # Получаем задачи в зависимости от авторизации
        if request.user.is_authenticated:
            tasks = Task.objects.filter(user=request.user)
        else:
            tasks = Task.objects.filter(is_private=False)

        # Создаем форму для отображения
        form = TaskForm()

        # Если это AJAX запрос, возвращаем JSON
        if request.headers.get('Accept') == 'application/json':
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data)

        # Иначе возвращаем HTML с контекстом
        return Response({
            'tasks': tasks,
            'form': form,
            'user': request.user
        })

    def post(self, request):
        """Обработка создания новой задачи"""
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            # Устанавливаем пользователя, если он авторизован
            if request.user.is_authenticated:
                task.user = request.user
            task.save()
            messages.success(request, 'Задача успешно создана!')
            return redirect('task-list-create')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')

        # Если форма невалидна, показываем ошибки
        if request.user.is_authenticated:
            tasks = Task.objects.filter(user=request.user)
        else:
            tasks = Task.objects.filter(is_private=False)

        return Response({
            'tasks': tasks,
            'form': form,
            'user': request.user,
            'errors': form.errors
        })


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "pages/task_detail.html"

    def get(self, request, *args, **kwargs):
        task = self.get_object()
        form = TaskForm(instance=task)

        return Response({
            'task': task,
            'form': form
        })

    def post(self, request, *args, **kwargs):
        task = self.get_object()

        # Проверяем кнопку удаления
        if "delete" in request.POST:
            task.delete()
            messages.success(request, 'Задача удалена!')
            return redirect("task-list-create")

        # Обновляем задачу
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Задача обновлена!')
            return redirect("task-list-create")

        return Response({
            'task': task,
            'form': form,
            'errors': form.errors
        })


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        if self.request.user.is_authenticated:
            context['user'] = self.request.user
        return context
