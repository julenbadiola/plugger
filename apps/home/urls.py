# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path

from apps.datatables.views import TransactionView
from apps.home import views
from apps.profile.views import profile_view

urlpatterns = [
    # The home page
    path("", views.index, name="home"),
    path("plugins.html", views.plugins, name="plugins"),
    path("settings/", profile_view, name="settings"),
    re_path(
        r"^transactions/(?:(?P<pk>\d+)/)?(?:(?P<action>\w+)/)?",
        TransactionView.as_view(),
        name="transactions",
    ),
    # Matches any html file
    re_path(r"^.*\.*", views.pages, name="pages"),
]
