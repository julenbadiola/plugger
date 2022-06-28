# -*- encoding: utf-8 -*-

from django.contrib.auth.models import User
from django.test import TestCase
from decouple import config
from django.test import tag

# https://medium.com/@adamking0126/a-simple-recipe-for-django-development-in-docker-bonus-testing-with-selenium-6a038ec19ba5

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

    @tag('integration')
    def test_redirect_on_authenticated(self):
        # get login page without being authenticated
        response = self.client.get('/login', follow=False)
        self.assertTrue(response.status_code == 200)

        # should be redirected when authenticated
        self.client.login(username=self.credentials["username"], password=self.credentials["password"])
        response2 = self.client.get('/login', follow=False)
        self.assertTrue(response2.status_code == 302)
  
    @tag('integration')
    def test_login_and_logout(self):
        # send login data
        response = self.client.post('/login', self.credentials, follow=True)
        # should be logged in now
        user = response.context['user']
        self.assertTrue(user.is_authenticated and user.is_active)
        self.assertEqual(response.status_code, 200)

        # send logout request
        response = self.client.post('/logout', follow=True)
        # should be unauthenticated now
        user = response.context['user']
        self.assertFalse(user.is_authenticated)
        self.assertEqual(response.status_code, 200)

    @tag('integration')
    def test_invalid_credentials(self):
        # send login data
        response = self.client.post('/login', {
            'username': "unknown",
            'password': ADMIN_PASSWORD,
        }, follow=True)
        # should be not logged in now
        user = response.context['user']
        self.assertFalse(user.is_authenticated)
        self.assertEqual(response.status_code, 401)
    
    @tag('integration')
    def test_invalid_login(self):
        # send login data
        response = self.client.post('/login', {
            'username': "unknown",
        }, follow=True)
        # should be not logged in now
        user = response.context['user']
        self.assertFalse(user.is_authenticated)
        self.assertEqual(response.status_code, 400)
