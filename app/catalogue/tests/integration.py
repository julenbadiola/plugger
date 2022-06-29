# -*- encoding: utf-8 -*-
from django.test import TestCase
from django.test import tag
from core.tests import TEST_CREDENTIALS
from catalogue.docker import manager

class CatalogueIntegrationTest(TestCase):
    def setUp(self):
        self.client.login(username=TEST_CREDENTIALS["username"], password=TEST_CREDENTIALS["password"])
        self.service_to_test = "drupal"

    @tag('integration')
    def test_catalogue_endpoint(self):
        # get catalogue in json format endpoint
        response = self.client.get('/json', follow=False)
        self.assertTrue(response.status_code == 200)
    
    @tag('integration')
    def test_status_endpoint(self):
        # get status endpoint
        response = self.client.get('/status', follow=False)
        self.assertTrue(response.status_code == 200)
    
    @tag('integration')
    def test_start_and_stop_service(self):
        # start and stop services
        self.assertFalse(self.service_to_test in [
                         container.name for container in manager.list()])
        response = self.client.post('/', data={
            "name": self.service_to_test
        })
        self.assertTrue(response.status_code == 200)
        self.assertTrue(self.service_to_test in [
                        container.name for container in manager.list()])

        response = self.client.post('/', data={
            "stop": self.service_to_test
        })
        self.assertTrue(response.status_code == 200)
        self.assertFalse(self.service_to_test in [
                        container.name for container in manager.list()])

        

