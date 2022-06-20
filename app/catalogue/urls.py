# -*- encoding: utf-8 -*-

from django.urls import path

from app.catalogue import views


urlpatterns = [
    path("", views.catalogue, name="catalogue"),
    path("json", views.catalogue_json, name="catalogue"),
    path("status", views.status, name="status"),
]
