from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from tasks import views

urlpatterns = ([
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('task/', include('tasks.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

])
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
              static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
