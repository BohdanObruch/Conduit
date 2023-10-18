from selene import browser, have, be

from demo_apps_project_tests.data.fake_data import generate_random_user_data
from demo_apps_project_tests.utils.sessions import conduit
from allure import step
from selene.support.shared.jquery_style import s


def register_user():
    user_data = generate_random_user_data()
    username = user_data["username"]
    email = user_data["email"]
    password = user_data["password"]
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


def registration_user():
    with step('Open main page'):
        browser.open('/')

    with step('Open register form'):
        with step('Click on Sign up'):
            s('[href="#/register"]').click()
        with step('Check page url'):
            browser.should(have.url_containing('#/register'))
        with step('Check page title'):
            browser.should(have.title('Sign up — Conduit'))

    with step('Fill in the form'):
        s('.auth-page form').should(be.visible)

        with step('Generate random user data'):
            user_data = generate_random_user_data()
        with step('Input username'):
            s('[ng-model$=username]').type(user_data["username"])
        with step('Input email'):
            s('[ng-model$=email]').type(user_data["email"])
        with step('Input password'):
            s('[ng-model$=password]').type(user_data["password"])

    with step('Submit the form'):
        s('[type=submit]').click()

    with step('Check user has been login'):
        with step('Checking the display of the username in the header'):
            s('.navbar').should(have.text(user_data["username"]))
    return user_data
