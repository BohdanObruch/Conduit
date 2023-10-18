from selene import browser, be, have
from allure import step
from demo_apps_project_tests.utils.sessions import conduit
from tests.conftest import dotenv
from selene.support.shared.jquery_style import s

email_user = dotenv.get('EMAIL')
password = dotenv.get('PASSWORD')
user_name = dotenv.get('USERNAME')


def login_user():
    with step('Open website'):
        browser.open('/')

    with step('Open login form'):
        with step('Click Sign In link in app header'):
            s('[href="#/login"]').click()

        with step('Checking the url of the page'):
            browser.should(have.url_containing('#/login'))

        with step('Checking the title of the page'):
            browser.should(have.title('Sign in — Conduit'))

    with step('Fill login form'):
        with step('Checking the display of the form'):
            s('.auth-page form').should(be.visible)

        with step('Fill the form'):
            with step('Fill email'):
                s('[ng-model$=email]').type(email_user)

            with step('Fill password'):
                s('[ng-model$=password]').type(password)

    with step('Submit form'):
        with step('Click Sign in button'):
            s('[type=submit]').click()

    with step('Check user has been login'):
        with step('Checking the display of the user name in the header'):
            s('.navbar').should(have.text(user_name))

        with step('Checking the url of the page'):
            browser.should(have.url_containing('/#/'))


def user_authorization():
    data = {
        "user": {
            "email": email_user,
            "password": password
        }
    }
    response = conduit().post('/users/login',
                              json=data
                              )
    assert response.status_code == 200
    user_data = response.json()["user"]
    return user_data
