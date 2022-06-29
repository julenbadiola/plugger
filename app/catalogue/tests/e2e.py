from core.tests import TEST_CREDENTIALS
from decouple import config
from django.conf import settings
from django.contrib.auth import (BACKEND_SESSION_KEY, HASH_SESSION_KEY,
                                 SESSION_KEY, get_user_model)
from django.contrib.sessions.backends.db import SessionStore
from django.test import TestCase, tag
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# https://stackoverflow.com/questions/22494583/login-with-code-when-using-liveservertestcase-with-django
# https://medium.com/@adamking0126/a-simple-recipe-for-django-development-in-docker-bonus-testing-with-selenium-6a038ec19ba5

ADMIN_USER = config('ADMIN_USER')
ADMIN_EMAIL = config('ADMIN_EMAIL')
ADMIN_PASSWORD = config('ADMIN_PASSWORD')

class CatalogueSeleniumTest(TestCase):
      def setUp(self):
             # First, get the superuser
            user = get_user_model()
            user.objects.get(username=ADMIN_USER)

            # Then create the authenticated session using the new user credentials
            session = SessionStore()
            session[SESSION_KEY] = user.pk
            session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
            session[HASH_SESSION_KEY] = user.get_session_auth_hash()
            session.save()

            # Finally, create the cookie dictionary
            cookie = {
                  'name': settings.SESSION_COOKIE_NAME,
                  'value': session.session_key,
                  'secure': False,
                  'path': '/',
            }
            
            # Create the selenium remote drivers
            self.chrome = webdriver.Remote(
                  command_executor='http://selenium_hub:4444/wd/hub',
                  desired_capabilities=DesiredCapabilities.CHROME
            )
            self.chrome.implicitly_wait(5)
            self.chrome.add_cookie(cookie)

            self.firefox = webdriver.Remote(
                  command_executor='http://selenium_hub:4444/wd/hub',
                  desired_capabilities=DesiredCapabilities.FIREFOX
            )
            self.firefox.implicitly_wait(5)
            self.firefox.add_cookie(cookie)

      def run_test(self, driver):
            driver.get('http://plugger:5005')
            self.assertIn(driver.title, 'Plugins | Plugger')
            
      @tag('e2e')
      def test_visit_site_with_chrome(self):
            self.run_test(self.chrome)
            
      @tag('e2e')
      def test_visit_site_with_firefox(self):
            self.run_test(self.firefox)
      
      def tearDown(self) -> None:
            self.chrome.quit()
            self.firefox.quit()
            return super().tearDown()
