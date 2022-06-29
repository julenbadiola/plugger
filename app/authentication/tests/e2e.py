from core.tests import TEST_CREDENTIALS
from django.test import TestCase, tag
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys


class AuthenticationSeleniumTest(TestCase):
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

      def run_test(self, driver):
            driver.get('http://plugger:5005')
            self.assertIn(driver.title, 'Login | Plugger')
            inputElement = driver.find_element_by_id("id_username")
            inputElement.send_keys(TEST_CREDENTIALS["username"])
            inputElement = driver.find_element_by_id("id_password")
            inputElement.send_keys(TEST_CREDENTIALS["password"])
            inputElement.send_keys(Keys.ENTER)
            self.firefox.implicitly_wait(5)
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
