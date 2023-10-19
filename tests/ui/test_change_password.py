from selene import browser, have
from demo_apps_project_tests.model.registration import registration_user
from allure import step
from selene.support.shared.jquery_style import s
from demo_apps_project_tests.helpers import app


def test_change_password(setup_browser):
    with step('Before'):
        user = registration_user()

    with step('Open settings form'):
        app.settings_form.going_to_settings()

    with step('Edit settings'):
        with step('Type new password'):
            s('[ng-model$=password]').type(user["password"])

    with step('Submit form'):
        s('[type="submit"]').with_(timeout=5).click()

    with step('Check updated settings'):
        with step('Checking url of the page'):
            browser.should(have.url_containing(f'/#/@{user["username"]}'))
        with step('Checking the display of the user name in the header'):
            s('.user-info [ng-bind$=username]').with_(timeout=5).should(have.text(user["username"]))
        with step('Checking the display of the user name in the user-info block'):
            s('.navbar').should(have.text(user["username"]))
