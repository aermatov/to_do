from django.urls import path

from users import views

urlpatterns = [
    path('register/', views.RegisterUserAPIView.as_view()),
]