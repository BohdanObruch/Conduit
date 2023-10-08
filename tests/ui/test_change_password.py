from selene import browser, be, have
from demo_apps_project_tests.model.registration import registration_user


def test_change_password(browser_management):
    # login_user()

    user = registration_user()

    browser.element('[href="#/settings"]').with_(timeout=5).click()
    browser.should(have.url_containing('/#/settings'))
    browser.element('.settings-page h1').should(have.text('Your Settings'))

    browser.element('[ng-submit*=submitForm]').should(be.visible)

    browser.element('[ng-model$=password]').type(user["password"])

    browser.element('[type="submit"]').with_(timeout=5).click()

    browser.should(have.url_containing(f'/#/@{user["username"]}'))
    browser.element('.user-info [ng-bind$=username]').with_(timeout=5).should(have.text(user["username"]))
    browser.element('.navbar').should(have.text(user["username"]))
