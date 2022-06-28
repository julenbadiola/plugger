# -*- encoding: utf-8 -*-
from django.test import TestCase
from catalogue.docker import manager
from django.test import tag
from catalogue.schema import ServiceModel
from catalogue.services import SERVICES_LIST, parse_and_add_data

class CatalogueTest(TestCase):
    invalid_data = {
                "configuration": {
                    "routing": {
                        "ports": [
                            {
                                "from": "8080/tcp",
                                "to": "8081"
                            }
                        ]
                    },
                    "environment": [
                        {
                            "key": "ALLOW_EMPTY_PASSWORD",
                            "value": "yes"
                        },
                        {
                            "key": "DRUPAL_DATABASE_USER",
                            "value": "##DRUPAL_MYSQL_USER##"
                        },
                        {
                            "key": "DRUPAL_DATABASE_PASSWORD",
                            "value": "##DRUPAL_MYSQL_PASSWORD##"
                        },
                        {
                            "key": "DRUPAL_DATABASE_HOST",
                            "value": "##DRUPAL_MYSQL_HOST##"
                        },
                        {
                            "key": "DRUPAL_DATABASE_NAME",
                            "value": "##DRUPAL_MYSQL_DATABASE##"
                        },
                        {
                            "key": "APACHE_HTTP_PORT_NUMBER",
                            "value": "8080"
                        }
                    ]
                },
                "variables": [],
                "network": "##PUBLIC_NETWORK##",
                "image": "bitnami/drupal:latest"
            }

    @tag('integration')
    def setUp(self):
        self.container_to_start = "wordpress"
        self.initialContainers = [
            container.name for container in manager.list()]

    
    @tag('integration')
    def start_service(self):
        self.assertFalse(self.container_to_start in [
                         container.name for container in manager.list()])
        manager.start(self.container_to_start,
                      SERVICES_LIST[self.container_to_start], {})
        self.assertTrue(self.container_to_start in [
                        container.name for container in manager.list()])
    
    @tag('integration')
    def stop_service(self):
        self.assertTrue(self.container_to_start in [
                        container.name for container in manager.list()])
        manager.remove(self.container_to_start)

        current_container_names = [
            container.name for container in manager.list()]
        self.assertFalse(self.container_to_start in current_container_names)
        self.assertListEqual(self.initialContainers, current_container_names)

    @tag('integration')
    def test_manager(self):
        self.start_service()
        self.stop_service()

    @tag('unit')
    def test_parse_invalid_service(self):
        with self.assertRaises(Exception):
            ServiceModel(**self.invalid_data)
        
        parse_and_add_data(self.invalid_data)
