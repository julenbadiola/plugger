# -*- encoding: utf-8 -*-

from django.urls import path

from apps.home import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # The home page
    path("", views.home, name="home"),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),
    path("plugins", views.plugins, name="plugins"),
    path("status", views.status, name="status"),
]
