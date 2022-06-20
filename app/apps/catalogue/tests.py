# -*- encoding: utf-8 -*-
from django.test import TestCase
from core.docker import manager
from core.catalogue import PLUGINS_LIST
from django.test import LiveServerTestCase
from selenium import webdriver
from django.contrib.auth import get_user_model
from seleniumlogin import force_login


class CatalogueTest(TestCase):
    def setUp(self):
        self.container_to_start = "wordpress"
        self.initialContainers = [
            container.name for container in manager.list()]

    def start_container(self):
        self.assertFalse(self.container_to_start in [
                         container.name for container in manager.list()])
        manager.start(self.container_to_start,
                      PLUGINS_LIST[self.container_to_start], {})
        self.assertTrue(self.container_to_start in [
                        container.name for container in manager.list()])

    def stop_container(self):
        self.assertTrue(self.container_to_start in [
                        container.name for container in manager.list()])
        manager.remove(self.container_to_start)

        current_container_names = [
            container.name for container in manager.list()]
        self.assertFalse(self.container_to_start in current_container_names)
        self.assertFalse(self.initialContainers == current_container_names)

    def test_manager(self):
        self.start_container()
        self.stop_container()


class CatalogueSeleniumTest(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Chrome()
        User = get_user_model()
        user = User.objects.create_user(username='admin', password='admin')
        force_login(user, selenium, live_server.url)
        self.selenium.get('http://127.0.0.1:5005/catalogue')

    def test_start_stop(self):
        # find the elements you need to submit form
        self.assertFalse(self.container_to_start in [container.name for container in manager.list()])
        start_wordpress_button = self.selenium.find_element_by_id('wordpressStartButton')
        start_wordpress_button.click()
        self.assertTrue(self.container_to_start in [container.name for container in manager.list()])
        self.selenium.refresh()
        
        stop_wordpress_button = self.selenium.find_element_by_id('wordpressStopButton')
        stop_wordpress_button.click()
        self.assertFalse(self.container_to_start in [container.name for container in manager.list()])

        # assert 'Lebron James' in self.selenium.page_source
