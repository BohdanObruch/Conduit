from allure import step
from demo_apps_project_tests.helpers import app


def test_open_article_detail_page(setup_browser):
    with step('Before'):
        app.website.open_website()

    with step('Open random article'):
        app.article_page.open_random_article()
