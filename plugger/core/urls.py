# -*- encoding: utf-8 -*-

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import handler404, handler500

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("apps.home.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler500 = 'core.errors.error_500'
handler404 = 'core.errors.error_404'
