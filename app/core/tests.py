from django.test.runner import DiscoverRunner as BaseRunner
from decouple import config
from django.contrib.auth import get_user_model
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed
import requests

# Get credentials from environment
ADMIN_USER = config('ADMIN_USER')
ADMIN_EMAIL = config('ADMIN_EMAIL')
ADMIN_PASSWORD = config('ADMIN_PASSWORD')
SELENIUM_HUB_HOST = config('SELENIUM_HUB_HOST')
SELENIUM_HUB_URI = f"http://{SELENIUM_HUB_HOST}/wd/hub"
SELENIUM_HUB_STATUS_URI = f"http://{SELENIUM_HUB_HOST}/status"

TEST_CREDENTIALS = {
            'username': ADMIN_USER,
            'password': ADMIN_PASSWORD,
            'email': ADMIN_EMAIL
        }


max_tries = 60 * 5  # 5 minutes
wait_seconds = 10

@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
)
def wait_for_selenium_hub() -> None:
    # print a dot in the same line on every iteration
    print(".", end =" ")

    res = requests.get(SELENIUM_HUB_STATUS_URI, timeout=3).json()
    if not res["value"]["ready"]:
        raise Exception("Selenium hub not ready yet")

    print("\nSelenium hub is ready!")

# https://stackoverflow.com/questions/52353962/django-initialize-data-test-for-all-test-classes

class MyMixinRunner(object):
    # Custom test runner
    def setup_databases(self, *args, **kwargs):
        temp_return = super(MyMixinRunner, self).setup_databases(*args, **kwargs)
        
        # Waits for selenium hub to be healthy
        print("------------------------------------")
        print("Waiting for selenium hub to be ready")
        wait_for_selenium_hub()
        # Creates a superuser using the environment variables
        print("------------------------------------")
        print("Creating a superuser for tests")
        user = get_user_model()
        user.objects.create_superuser(**TEST_CREDENTIALS)
        print("Done!")
        print("------------------------------------")

        return temp_return

    def teardown_databases(self, *args, **kwargs):
        return super(MyMixinRunner, self).teardown_databases(*args, **kwargs)

class MyTestRunner(MyMixinRunner, BaseRunner):
    pass