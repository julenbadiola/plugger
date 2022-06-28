# -*- encoding: utf-8 -*-

from django.urls import path

from authentication import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("login", views.user_login, name="login"),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),
]
