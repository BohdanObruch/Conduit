import os

import pytest
from selene import browser

from selenium import webdriver as webdriver_selenium
from selenium.webdriver.chrome.options import Options
from demo_apps_project_tests.controls import attach
from dotenv import dotenv_values, load_dotenv


@pytest.fixture(scope='session', autouse=True)
def env():
    load_dotenv()


dotenv = dotenv_values()

web_url = dotenv.get('WEB_URL')


@pytest.fixture(scope='function')
def browser_management():
    browser.config.base_url = web_url
    browser.config.browser_name = os.getenv('selene.browser_name', 'chrome')
    browser.config.hold_browser_open = (
            os.getenv('selene.hold_browser_open', 'false').lower() == 'true'
    )
    browser.config.timeout = float(os.getenv('selene.timeout', '4'))
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.quit()


DEFAULT_BROWSER_VERSION = "116.0"
DEFAULT_BROWSER = 'chrome'


def pytest_addoption(parser):
    parser.addoption(
        '--browser_name',
        default=DEFAULT_BROWSER,
        help='web: browser (chrome | firefox)'
    )

    parser.addoption(
        '--browser_version',
        default=DEFAULT_BROWSER_VERSION,
        help='web: browser version (if chrome: 110.0, 112.0; firefox: 110.0, 112.0)'
    )


@pytest.fixture(scope='session')
def get_option_browser_name(request):
    return request.config.getoption('--browser_name')


@pytest.fixture(scope='session')
def get_option_browser_version(request):
    return request.config.getoption('--browser_version')


@pytest.fixture(scope='function')
def setup_browser(request, get_option_browser_name, get_option_browser_version):
    browser.config.base_url = os.getenv('selene.base_url', web_url)
    browser.config.window_width = 1920
    browser.config.window_height = 1080

    browser_name = get_option_browser_name
    browser_name = browser_name if browser_name != '' else DEFAULT_BROWSER

    browser_version = get_option_browser_version
    browser_version = browser_version if browser_version != "" else DEFAULT_BROWSER_VERSION

    options = Options()
    selenoid_capabilities = {
        "browserName": browser_name,
        "browserVersion": browser_version,
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)

    url = os.getenv('URL')

    driver = webdriver_selenium.Remote(
        command_executor=f"{url}/wd/hub",
        options=options
    )
    browser.config.driver = driver
    yield browser

    attach.add_html(browser)
    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_video_selenoid(browser)
    browser.quit()
