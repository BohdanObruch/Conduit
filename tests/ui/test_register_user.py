import os

from selene import browser, be, have
from demo_apps_project_tests.data.fake_data import username, email, password


def test_user_registration():
    browser.open('/')
    browser.element('[href="#/register"]').click()
    browser.should(have.url_containing('#/register'))
    browser.should(have.title('Sign up — Conduit'))
    browser.element('.auth-page form').should(be.visible)
    browser.element('[ng-model$=username]').type(username)
    browser.element('[ng-model$=email]').type(email)
    browser.element('[ng-model$=password]').type(password)
    browser.element('[type=submit]').click()
    browser.element('.navbar').should(have.text(username))





