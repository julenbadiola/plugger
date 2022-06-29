# -*- encoding: utf-8 -*-

from django.test import TestCase, tag
from core.tests import TEST_CREDENTIALS

class AuthenticationIntegrationTest(TestCase):
    
    @tag('integration')
    def test_redirect_on_authenticated(self):
        # get login page without being authenticated
        response = self.client.get('/login', follow=False)
        self.assertTrue(response.status_code == 200)
        self.assertTemplateUsed(response, template_name='login.html')

        # should be redirected to catalogue when authenticated
        self.client.login(
            username=TEST_CREDENTIALS["username"], password=TEST_CREDENTIALS["password"])
        response2 = self.client.get('/login')
        self.assertTrue(response2.status_code == 302)

    @tag('integration')
    def test_login_and_logout(self):
        # send login data
        response = self.client.post('/login', TEST_CREDENTIALS, follow=True)
        self.assertTemplateUsed(response, template_name='catalogue.html')
        # should be logged in now
        user = response.context['user']
        self.assertTrue(user.is_authenticated and user.is_active)
        self.assertEqual(response.status_code, 200)

        # send logout request
        response = self.client.post('/logout', follow=True)
        # should be unauthenticated now and login page been rendered
        user = response.context['user']
        self.assertTemplateUsed(response, template_name='login.html')
        self.assertFalse(user.is_authenticated)
        self.assertEqual(response.status_code, 200)

    @tag('integration')
    def test_invalid_credentials(self):
        # send login data
        response = self.client.post('/login', {
            'username': "invalid",
            'password': TEST_CREDENTIALS["password"],
        }, follow=True)
        # should be not logged in yet and login page rendered
        user = response.context['user']
        self.assertFalse(user.is_authenticated)
        self.assertEqual(response.status_code, 401)
        self.assertTemplateUsed(response, template_name='login.html')

    @tag('integration')
    def test_invalid_login(self):
        # send login data
        response = self.client.post('/login', {
            'username': "invalid",
        }, follow=True)
        # should be not logged in yet and login page rendered
        user = response.context['user']
        self.assertFalse(user.is_authenticated)
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, template_name='login.html')
