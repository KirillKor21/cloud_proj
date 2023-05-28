from django.contrib import admin
from django.http import request
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('films/', include('films.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls'))
]
