# -*- encoding: utf-8 -*-

from django.contrib.auth.models import User
from django.test import TestCase
from decouple import config

ADMIN_USER = config('ADMIN_USER')
ADMIN_EMAIL = config('ADMIN_EMAIL')
ADMIN_PASSWORD = config('ADMIN_PASSWORD')

class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': ADMIN_USER,
            'password': ADMIN_PASSWORD,
            'email': ADMIN_EMAIL
        }
        User.objects.create_superuser(**self.credentials)

    def test_login(self):
        # send login data
        response = self.client.post('/login', self.credentials, follow=True)
        # should be logged in now
        user = response.context['user']
        self.assertTrue(user.is_authenticated and user.is_active)

    def test_logout(self):
        # send login data
        response = self.client.post('/logout', follow=True)
        # should be unauthenticated now
        user = response.context['user']
        self.assertFalse(user.is_authenticated)