# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path

from apps.home import views
from apps.profile.views import profile_view
from django.conf.urls import url, include, handler404, handler500


urlpatterns = [
    # The home page
    path("", views.index, name="home"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("plugins", views.plugins, name="plugins"),
    path("settings/", profile_view, name="settings"),
]
