import os
from demo_apps_project_tests.utils.requests_helper import BaseSession

api_url = os.getenv('API_URL')


def conduit() -> BaseSession:
    return BaseSession(base_url=api_url)
