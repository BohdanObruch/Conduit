from selene import browser, have, command

from demo_apps_project_tests.data.fake_data import generate_random_article
from demo_apps_project_tests.model.authorization import login_user
from demo_apps_project_tests.model.article import open_random_article


def test_delete_comment(browser_management):
    login_user()

    browser.element('.feed-toggle ul > li:nth-child(2) a').click().should(have.css_class('active'))

    open_random_article()
    comment = generate_random_article()
    browser.element('textarea[ng-model$=body]').perform(command.js.scroll_into_view).click().type(comment["comments"])
    browser.element('button[type=submit]').click()
    browser.element('comment .card').perform(command.js.scroll_into_view)
    browser.all('.article-page comment').element_by_its('p', have.text(comment["comments"]))

    delete_comment = browser.all('.article-page comment').with_(timeout=5).element_by_its('p',
                                                                                          have.exact_text(
                                                                                              comment["comments"]))
    delete_comment.element('.card-footer [ng-click*="delete"]').click()

    delete_comment.should(have.no.visible)
