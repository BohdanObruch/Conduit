from demo_apps_project_tests.model.authorization import login_user
from allure import step
from demo_apps_project_tests.helpers import app


def test_publish_article(setup_browser):
    with step('Before'):
        login_user()

    with step('Open editor'):
        app.article_page.open_add_new_article_page()

    with step('Fill form'):
        with step('Fill article'):
            article = app.article_page.fill_article()

    with step('Check article data'):
        app.article_page.check_article_data(article)
