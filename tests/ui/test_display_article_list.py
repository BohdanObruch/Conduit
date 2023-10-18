from demo_apps_project_tests.helpers import app
from allure import step


def test_display_article_list(browser_management):
    with step('Before'):
        app.website.open_website()

    with step('Check article list'):
        app.article_page.check_article_list()

    with step('Check article card'):
        app.article_page.check_articles()
