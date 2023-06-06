from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('films/', include('films.urls')),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
