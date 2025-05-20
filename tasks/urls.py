from django.urls import path

from tasks import views

urlpatterns = [
    path("", views.get_index, name="index"),
]