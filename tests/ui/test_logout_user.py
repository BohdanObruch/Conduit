from selene import browser, be, have, command
from tests.conftest import dotenv

email = dotenv.get('EMAIL')
password = dotenv.get('PASSWORD')
username = dotenv.get('USERNAME')


def test_logout_user():
    browser.open('/')

    browser.element('[href="#/login"]').click()

    browser.should(have.url_containing('#/login'))
    browser.should(have.title('Sign in — Conduit'))
    browser.element('.auth-page form').should(be.visible)

    browser.element('[ng-model$=email]').type(email)
    browser.element('[ng-model$=password]').type(password)
    browser.element('[type=submit]').click()

    browser.element('.navbar').should(have.text(username))

    browser.element('[href$="/settings"]').click()

    browser.element('.settings-page h1').should(have.text('Your Settings'))

    browser.element('.settings-page [ng-click*=logout]').perform(command.js.scroll_into_view).click()

    browser.element('.navbar').should(have.no.text(username))







