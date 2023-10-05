from demo_apps_project_tests.data.fake_data import generate_random_user_data
from demo_apps_project_tests.utils.sessions import conduit


def register_user():
    user_data = generate_random_user_data()
    username = user_data["username"]
    email = user_data["email"]
    password = user_data["password"]
    data = {
        "user": {
            "username": username,
            "email": email,
            "password": password
        }
    }
    response = conduit().post('/users',
                              json=data
                              )
    assert response.status_code == 201
    user_token = response.json()["user"]["token"]
    return user_token
