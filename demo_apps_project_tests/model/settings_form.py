from selene import browser
from demo_apps_project_tests.data.fake_data import generate_random_user_data


def clear_form():
    browser.element('[ng-model$=image] ').clear()
    browser.element('[ng-model$=username]').clear()
    browser.element('[ng-model$=bio]').clear()
    browser.element('[ng-model$=email]').clear()
    browser.element('[ng-model$=password]').clear()


def fill_settings():
    user = generate_random_user_data()
    browser.element('[ng-model$=image] ').type(user["picture"])
    browser.element('[ng-model$=username]').type(user["username"])
    browser.element('[ng-model$=bio]').type(user["bio"])
    browser.element('[ng-model$=email]').type(user["email"])

    browser.element('[type="submit"]').with_(timeout=5).click()
    return user
