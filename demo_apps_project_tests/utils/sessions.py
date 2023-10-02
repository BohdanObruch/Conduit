import os
from demo_apps_project_tests.utils.requests_helper import BaseSession
from dotenv import load_dotenv

def conduit() -> BaseSession:
    api_url = os.getenv('API_URL')
    return BaseSession(base_url=api_url)


