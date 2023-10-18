from selene import browser, have
from allure import step
from selene.support.shared.jquery_style import s
from demo_apps_project_tests.model.authorization import user_name


class Website:
    def open_website(self):
        with step('Open website'):
            browser.open('/')
        with step('Checking the url'):
            browser.should(have.url_containing('/#/'))
        return self

    def go_to_home_page(self):
        with step('Go to Home page'):
            s('.navbar [show-authed="true"] a[href="#/"]').click()
        with step('Checking the url'):
            browser.should(have.url_containing('/#/'))
        return self

    def going_to_user_page(self):
        with step('Click on the user name button'):
            s(f'.navbar [href="#/@{user_name}"]').with_(timeout=5).click()
        with step('Url contains user name'):
            browser.should(have.url_containing(f'/#/@{user_name}'))
        return self
