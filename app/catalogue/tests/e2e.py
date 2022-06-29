import time

from core.tests import SELENIUM_HUB_URI, TEST_CREDENTIALS
from django.conf import settings
from django.contrib.auth import (BACKEND_SESSION_KEY, HASH_SESSION_KEY,
                                 SESSION_KEY, get_user_model)
from django.contrib.sessions.backends.db import SessionStore
from django.test import TestCase, tag
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# https://stackoverflow.com/questions/22494583/login-with-code-when-using-liveservertestcase-with-django
# https://medium.com/@adamking0126/a-simple-recipe-for-django-development-in-docker-bonus-testing-with-selenium-6a038ec19ba5

class CatalogueSeleniumTest(TestCase):
      def setUp(self):
             # First, get the superuser
            user = get_user_model()
            superuser = user.objects.get(username=TEST_CREDENTIALS["username"])

            # Then create the authenticated session using the new user credentials
            session = SessionStore()
            session[SESSION_KEY] = superuser.pk
            session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
            session[HASH_SESSION_KEY] = superuser.get_session_auth_hash()
            session.save()

            # Finally, create the cookie dictionary
            self.cookie = {
                  'name': settings.SESSION_COOKIE_NAME,
                  'value': session.session_key,
                  'secure': False,
                  'path': '/',
            }

            # Create the selenium remote drivers
            self.chrome = webdriver.Remote(
                  command_executor=SELENIUM_HUB_URI,
                  desired_capabilities=DesiredCapabilities.CHROME
            )
            self.chrome.implicitly_wait(5)

            self.firefox = webdriver.Remote(
                  command_executor=SELENIUM_HUB_URI,
                  desired_capabilities=DesiredCapabilities.FIREFOX
            )
            self.firefox.implicitly_wait(5)


      def run_test(self, driver, service_to_test):
            driver.get('http://plugger:5005')
            driver.add_cookie(self.cookie)
            driver.refresh()
            driver.get('http://plugger:5005')

            self.assertIn(driver.title, 'Catalogue | Plugger')
            
            openModalButton = driver.find_element_by_id(f"{service_to_test}OpenButton")
            openModalButton.click()

      @tag('e2e')
      def test_visit_site_with_chrome(self):
            self.run_test(self.chrome, "wordpress")
            
      @tag('e2e')
      def test_visit_site_with_firefox(self):
            self.run_test(self.firefox, "drupal")
      
      def tearDown(self) -> None:
            self.chrome.quit()
            self.firefox.quit()
            return super().tearDown()
