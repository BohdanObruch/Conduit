from selene import browser, have, command, be

from demo_apps_project_tests.data.fake_data import generate_random_user_data
from demo_apps_project_tests.model.authorization import login_user, user_name
from allure import step
from selene.support.shared.jquery_style import s
from tests.conftest import dotenv


email_user = dotenv.get('EMAIL')
password = dotenv.get('PASSWORD')
username = dotenv.get('USERNAME')


def test_registration_user(setup_browser):
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


def test_login_user(setup_browser):
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
            s('.navbar').should(have.text(username))
        with step('Checking the url of the page'):
            browser.should(have.url_containing('/#/'))


def test_logout_user(setup_browser):
    with step('Before'):
        login_user()

    with step('Logout user'):
        with step('Click on settings button'):
            s('[href$="/settings"]').click()
        with step('Checking page header'):
            s('.settings-page h1').should(have.text('Your Settings'))
        with step('Click on logout button'):
            s('.settings-page [ng-click*=logout]').perform(command.js.scroll_into_view).click()
        with step('Checking the no display of the user name in the header'):
            s('.navbar').should(have.no.text(user_name))
