from allure import step
from demo_apps_project_tests.model.authorization import login_user
from demo_apps_project_tests.helpers import app


def test_subscribe_to_user(setup_browser):
    with step('Before'):
        login_user()

    with step('Delete all my articles'):
        app.article_page.deleting_created_posts()

    with step('Checking for a subscription'):
        app.website.go_to_home_page()
        app.article_page.go_to_your_feed_tab()

    with step('Unsubscribe from user by unfollowing him'):
        app.article_page.unfollow_subscriptions()

    with step('Subscribe to user by following him'):
        app.article_page.follow_subscriptions()
