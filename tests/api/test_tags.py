from schemas.conduit import *
from pytest_voluptuous import S
from demo_apps_project_tests.utils.sessions import conduit
from allure import tag, title


@tag('API')
@title("Get tags")
def test_get_tags():
    response = conduit().get('/tags')
    assert response.status_code == 200
    assert S(tags) == response.json()
