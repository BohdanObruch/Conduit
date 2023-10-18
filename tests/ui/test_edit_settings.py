from selene import browser, be, have
from demo_apps_project_tests.model.registration import registration_user
from allure import step
from selene.support.shared.jquery_style import s
from demo_apps_project_tests.helpers import app


def test_edit_settings(browser_management):
    with step('Before'):
        registration_user()

    with step('Open settings form'):
        app.settings_form.going_to_settings()

    with step('Edit settings'):
        with step('Checking the display of the form'):
            s('[ng-submit*=submitForm]').should(be.visible)
        with step('All data in the form is cleared'):
            app.settings_form.clear_form()
        with step('Filling new data in the form'):
            user = app.settings_form.fill_settings()
    with step('Check updated settings'):
        with step('Checking url of the page'):
            user_bio = user["bio"].replace("\n", " ")
            browser.should(have.url_containing(f'/#/@{user["username"]}'))
        with step('Checking the display of the user name in the header'):
            s('.user-info [ng-bind$=username]').with_(timeout=5).should(have.text(user["username"]))
        with step('Checking the display of the user bio in the header'):
            s('.user-info [ng-bind$=bio]').should(have.text(user_bio))
        with step('Checking the display of the user image in the header'):
            s('.user-info img').should(have.attribute('src', user["picture"]))
