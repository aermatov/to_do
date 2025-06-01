from django.urls import path
from .views import TaskListCreateView, TaskDetailView, index

urlpatterns = [
    path('', index, name='index'),
    path('api/tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('api/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
]
