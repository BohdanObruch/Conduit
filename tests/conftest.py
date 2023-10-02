import os
import time

import pytest
from demo_apps_project_tests.utils.sessions import conduit
from selene.support.shared import browser
from selenium import webdriver as webdriver_selenium
from selenium.webdriver.chrome.options import Options
from dotenv import dotenv_values, load_dotenv
from demo_apps_project_tests.data.fake_data import generate_random_article_data, generate_random_user_data


@pytest.fixture(scope='session', autouse=True)
def env():
    load_dotenv()


dotenv = dotenv_values()

user_email = dotenv.get('EMAIL')
user_password = dotenv.get('PASSWORD')
slug = dotenv.get('SLUG')


#
# @pytest.fixture(scope='function', autouse=True)
# def browser_management():
#     browser.config.base_url = os.getenv('selene.base_url', web_url)
#     browser.config.browser_name = os.getenv('selene.browser_name', 'chrome')
#     browser.config.hold_browser_open = (
#             os.getenv('selene.hold_browser_open', 'false').lower() == 'true'
#     )
#     browser.config.timeout = float(os.getenv('selene.timeout', '3'))
#     browser.config.window_width = 1920
#     browser.config.window_height = 1080
#
#
# DEFAULT_BROWSER_VERSION = "110.0"
#
#
# def pytest_addoption(parser):
#     parser.addoption(
#         '--browser_version',
#         default='110.0'
#     )
#
#
# @pytest.fixture(scope='function')
# def setup_browser(request):
#     browser_version = request.config.getoption('--browser_version')
#     browser_version = browser_version if browser_version != "" else DEFAULT_BROWSER_VERSION
#     options = Options()
#     selenoid_capabilities = {
#         "browserName": "chrome",
#         "browserVersion": browser_version,
#         "selenoid:options": {
#             "enableVNC": True,
#             "enableVideo": True
#         }
#     }
#     options.capabilities.update(selenoid_capabilities)
#
#     url = os.getenv('URL')
#
#     driver = webdriver_selenium.Remote(
#         command_executor=f"{url}/wd/hub",
#         options=options
#     )
#     browser.config.driver = driver
#     yield browser
#
#     attach.add_html(browser)
#     attach.add_screenshot(browser)
#     attach.add_logs(browser)
#     attach.add_video_selenoid(browser)
#     browser.quit()


# @pytest.fixture()
# def register_user(username=None, email=None, password=None):
#     data = {
#         "user": {
#             "username": username or generate_random_user_data()[0],
#             "email": email or generate_random_user_data()[1],
#             "password": password or generate_random_user_data()[2]
#         }
#     }
#     response = conduit().post('/users',
#                               json=data
#                               )
#     assert response.status_code == 201
#     token = response.json()["user"]["token"]
#     user_name = response.json()["user"]["username"]
#     user_email = response.json()["user"]["email"]
#     return token, user_name, user_email

@pytest.fixture()
def register_user():
    username = generate_random_user_data()[0]
    email = generate_random_user_data()[1]
    password = generate_random_user_data()[2]
    data = {
        "user": {
            "username": username,
            "email": email,
            "password": password
        }
    }
    response = conduit().post('/users',
                              json=data
                              )
    assert response.status_code == 201
    user_token = response.json()["user"]["token"]
    return user_token


@pytest.fixture()
def user_authorization():
    data = {
        "user": {
            "email": user_email,
            "password": user_password
        }
    }
    response = conduit().post('/users/login',
                              json=data
                              )
    assert response.status_code == 200
    token = response.json()["user"]["token"]
    email = response.json()["user"]["email"]
    username = response.json()["user"]["username"]
    return token, email, username


@pytest.fixture()
def create_article(user_authorization):
    title_article = generate_random_article_data()[0]
    description_article = generate_random_article_data()[1]
    body_article = generate_random_article_data()[2]
    tags_article = generate_random_article_data()[3]
    token = user_authorization[0]
    data = {
        "article": {
            "title": title_article,
            "description": description_article,
            "body": body_article,
            "tagList": tags_article,
        }
    }

    headers = {
        'Authorization': f'Token {token}'
    }
    response = conduit().post(f'/articles',
                              headers=headers,
                              json=data
                              )
    assert response.status_code == 201
    slug_article = response.json()["article"]["slug"]
    return slug_article, token


@pytest.fixture()
def create_a_comment_for_article(user_authorization):
    body_article = generate_random_article_data()[2]
    token = user_authorization[0]
    data = {
        "comment": {
            "body": body_article}
            }
    headers = {
        'Authorization': f'Token {token}'
    }
    response = conduit().post(f'/articles/{slug}/comments',
                              headers=headers,
                              json=data
                              )
    assert response.status_code == 200
    id_comment = response.json()["comment"]["id"]
    return id_comment, token
