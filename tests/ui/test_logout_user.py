from selene import have, command
from demo_apps_project_tests.model.authorization import login_user, user_name
from allure import step
from selene.support.shared.jquery_style import s


def test_logout_user(browser_management):
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
