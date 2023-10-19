from demo_apps_project_tests.model.authorization import login_user
from demo_apps_project_tests.helpers import app
from allure import step


def test_add_comment(setup_browser):
    with step('Before'):
        login_user()

    with step('Open random article'):
        with step('Go to global feed tab'):
            app.article_page.go_to_global_feed_tab()
        with step('Open random article'):
            app.article_page.open_random_article()

    with step('Add comment'):
        app.article_page.add_comment()
