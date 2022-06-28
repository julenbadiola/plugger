#!/bin/bash

coverage run -p ./manage.py test --exclude-tag=e2e
# coverage run -p ./manage.py test --tag=e2e
coverage combine
coverage report
coverage html
coverage xml