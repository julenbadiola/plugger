# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models


class Data(models.Model):

    type = models.CharField(
        max_length=35, choices=[("product", "product"), ("transaction", "transaction")]
    )
    name = models.CharField(max_length=35)
    value = models.IntegerField()
    ts = models.DateTimeField(auto_now=True)
