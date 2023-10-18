from demo_apps_project_tests.data.fake_data import generate_random_user_data
from selene.support.shared.jquery_style import s
from allure import step
from selene import browser, be, have


class SettingsForm:
    def clear_form(self):
        with step('Clear form'):
            s('[ng-model$=image] ').clear()
            s('[ng-model$=username]').clear()
            s('[ng-model$=bio]').clear()
            s('[ng-model$=email]').clear()
            s('[ng-model$=password]').clear()
        return self

    @staticmethod
    def fill_settings():
        with step('Generate random user data'):
            user = generate_random_user_data()
        with step('Fill the form'):
            s('[ng-model$=image] ').type(user["picture"])
            s('[ng-model$=username]').type(user["username"])
            s('[ng-model$=bio]').type(user["bio"])
            s('[ng-model$=email]').type(user["email"])

        with step('Submit form'):
            with step('Click Update Settings button'):
                s('[type="submit"]').with_(timeout=5).click()
        return user

    def going_to_settings(self):
        with step('Click Settings link in app header'):
            s('[href="#/settings"]').with_(timeout=5).click()
        with step('Checking the url of the page'):
            browser.should(have.url_containing('/#/settings'))
        with step('Checking the title of the page'):
            s('.settings-page h1').should(have.text('Your Settings'))
        with step('Checking the display of the form'):
            s('[ng-submit*=submitForm]').should(be.visible)
        return self
