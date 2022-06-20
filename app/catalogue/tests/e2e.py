from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from django.test import tag

# PRUEBA ESTE https://github.com/mzdaniel/django-selenium-test-runner/blob/master/tests/polls/tests/selenium/test_complete.py

class SeleniumTest(TestCase):
      @tag('e2e')
      def setUp(self):
            self.chrome = webdriver.Remote(
                  command_executor='http://selenium_hub:4444/wd/hub',
                  desired_capabilities=DesiredCapabilities.CHROME
            )
            self.chrome.implicitly_wait(5)
            self.firefox = webdriver.Remote(
                  command_executor='http://selenium_hub:4444/wd/hub',
                  desired_capabilities=DesiredCapabilities.FIREFOX
            )
            self.firefox.implicitly_wait(5)

      @tag('e2e')
      def test_visit_site_with_chrome(self):
            self.chrome.get('http://plugger:5005')
            self.assertIn(self.firefox.title, 'Plugins | Plugger')
            
      @tag('e2e')
      def test_visit_site_with_firefox(self):
            self.firefox.get('http://plugger:5005')
            self.assertIn(self.firefox.title, 'Plugins | Plugger')