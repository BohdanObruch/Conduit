from selene import browser, be, have
from demo_apps_project_tests.model.authorization import login_user
from demo_apps_project_tests.model.registration import registration_user
from demo_apps_project_tests.model.settings_form import clear_form, fill_settings


def test_edit_settings(browser_management):
    # login_user()
    registration_user()

    browser.element('[href="#/settings"]').with_(timeout=5).click()
    browser.should(have.url_containing('/#/settings'))
    browser.element('.settings-page h1').should(have.text('Your Settings'))

    browser.element('[ng-submit*=submitForm]').should(be.visible)
    clear_form()

    user = fill_settings()
    user_bio = user["bio"].replace("\n", " ")
    browser.should(have.url_containing(f'/#/@{user["username"]}'))
    browser.element('.user-info [ng-bind$=username]').with_(timeout=5).should(have.text(user["username"]))
    browser.element('.user-info [ng-bind$=bio]').should(have.text(user_bio))
    browser.element('.user-info img').should(have.attribute('src', user["picture"]))






