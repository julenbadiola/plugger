# -*- encoding: utf-8 -*-

from django.test import TestCase
from django.test import tag
from django.contrib.auth import get_user_model
from core.tests import TEST_CREDENTIALS

class AuthenticationUnitTest(TestCase):
    @tag('unit')
    def test_superuser_creation(self):
        credentials = {
            'username': "random",
            'password': "random",
            'email': "random@mail.com"
        }
        user = get_user_model()
        user.objects.create_superuser(**credentials)
        user = user.objects.get(username=credentials["username"])    
        self.assertTrue(user is not None)

    @tag('unit')
    def test_superuser_created_from_env(self):
        # check core.tests TestRunner, which creates a superuser before running the tests
        user = get_user_model()
        user = user.objects.get(username=TEST_CREDENTIALS["username"])    
        self.assertTrue(user is not None)