from django.test.runner import DiscoverRunner as BaseRunner
from decouple import config
from django.contrib.auth import get_user_model

ADMIN_USER = config('ADMIN_USER')
ADMIN_EMAIL = config('ADMIN_EMAIL')
ADMIN_PASSWORD = config('ADMIN_PASSWORD')

TEST_CREDENTIALS = {
            'username': ADMIN_USER,
            'password': ADMIN_PASSWORD,
            'email': ADMIN_EMAIL
        }

# Test runner that creates a superuser from the ENV variables before starting the tests
# https://stackoverflow.com/questions/52353962/django-initialize-data-test-for-all-test-classes

class MyMixinRunner(object):
    def setup_databases(self, *args, **kwargs):
        temp_return = super(MyMixinRunner, self).setup_databases(*args, **kwargs)
        
        user = get_user_model()
        user.objects.create_superuser(**TEST_CREDENTIALS)
        return temp_return

    def teardown_databases(self, *args, **kwargs):
        return super(MyMixinRunner, self).teardown_databases(*args, **kwargs)

class MyTestRunner(MyMixinRunner, BaseRunner):
    pass