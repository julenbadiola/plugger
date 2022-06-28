# -*- encoding: utf-8 -*-
from django.test import TestCase
from django.test import tag
from decouple import config
from django.contrib.auth.models import User

ADMIN_USER = config('ADMIN_USER')
ADMIN_EMAIL = config('ADMIN_EMAIL')
ADMIN_PASSWORD = config('ADMIN_PASSWORD')

class CatalogueIntegrationTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': ADMIN_USER,
            'password': ADMIN_PASSWORD,
            'email': ADMIN_EMAIL
        }
        User.objects.create_superuser(**self.credentials)
        self.client.login(username=self.credentials["username"], password=self.credentials["password"])

    @tag('integration')
    def test_catalogue_endpoint(self):
        # get home page without being authenticated
        response = self.client.get('/json', follow=False)
        self.assertTrue(response.status_code == 200)
    
    @tag('integration')
    def test_status_endpoint(self):
        # get home page without being authenticated
        response = self.client.get('/status', follow=False)
        self.assertTrue(response.status_code == 200)
    
    @tag('integration')
    def test_start_and_stop_service(self):
        # get home page without being authenticated
        response = self.client.post('/', data={
            "name": "drupal"
        })
        print(response.json())
        self.assertTrue(response.status_code == 200)
        

