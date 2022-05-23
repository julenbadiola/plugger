# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from import_export import resources
from import_export.admin import ImportMixin

from apps.home.models import Data


class TransactionResource(resources.ModelResource):
    class Meta:
        model = Data
        fields = ["id", "type", "name", "value", "ts"]


@admin.register(Data)
class TransactionAdmin(ImportMixin, admin.ModelAdmin):
    list_display = ["id", "type", "name", "value", "ts"]
    resource_class = TransactionResource
