from selene import browser, be, have

from demo_apps_project_tests.utils.sessions import conduit
from tests.conftest import dotenv

email_user = dotenv.get('EMAIL')
password = dotenv.get('PASSWORD')
user_name = dotenv.get('USERNAME')


def login_user():
    browser.open('/')

    browser.element('[href="#/login"]').click()

    browser.should(have.url_containing('#/login'))
    browser.should(have.title('Sign in — Conduit'))

    browser.element('.auth-page form').should(be.visible)
    browser.element('[ng-model$=email]').type(email_user)
    browser.element('[ng-model$=password]').type(password)
    browser.element('[type=submit]').click()

    browser.element('.navbar').should(have.text(user_name))


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
