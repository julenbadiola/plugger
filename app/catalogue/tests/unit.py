# -*- encoding: utf-8 -*-
from django.test import TestCase
from core.docker import manager
from core.services import SERVICES_LIST

# https://devblogs.microsoft.com/python/announcing-playwright-for-python-reliable-end-to-end-testing-for-the-web/

class CatalogueTest(TestCase):
    def setUp(self):
        self.container_to_start = "wordpress"
        self.initialContainers = [
            container.name for container in manager.list()]

    def start_service(self):
        self.assertFalse(self.container_to_start in [
                         container.name for container in manager.list()])
        manager.start(self.container_to_start,
                      SERVICES_LIST[self.container_to_start], {})
        self.assertTrue(self.container_to_start in [
                        container.name for container in manager.list()])

    def stop_service(self):
        self.assertTrue(self.container_to_start in [
                        container.name for container in manager.list()])
        manager.remove(self.container_to_start)

        current_container_names = [
            container.name for container in manager.list()]
        self.assertFalse(self.container_to_start in current_container_names)
        self.assertListEqual(self.initialContainers, current_container_names)

    def test_manager(self):
        self.start_service()
        self.stop_service()