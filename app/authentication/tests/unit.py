# -*- encoding: utf-8 -*-

from django.contrib.auth.models import User
from django.test import TestCase
from django.test import tag

class LogInTest(TestCase):
    @tag('unit')
    def create_admin(self):
        credentials = {
            'username': "random",
            'password': "random",
            'email': "random@mail.com"
        }
        User.objects.create_superuser(**credentials)
        user = User.objects.get(username=credentials["username"])    
        self.assertTrue(user is not None)