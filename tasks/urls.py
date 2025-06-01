from django.urls import path
from .views import TaskListCreateView, TaskDetailView

urlpatterns = [
    path('', TaskListCreateView.as_view(), name='task-list-create'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('api/tasks/', TaskListCreateView.as_view(), name='api-task-list'),
    path('api/task/<int:pk>/', TaskDetailView.as_view(), name='api-task-detail'),
]
