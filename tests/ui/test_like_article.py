from demo_apps_project_tests.model.authorization import login_user
from allure import step
from demo_apps_project_tests.helpers import app


def test_like_article(browser_management):
    with step('Before'):
        login_user()

        with step('Open global feed tab'):
            app.article_page.go_to_global_feed_tab()

    with step('Select random article'):
        app.article_page.open_random_article()

    with step('Like/unlike article'):
        app.article_page.like_unlike_article()
