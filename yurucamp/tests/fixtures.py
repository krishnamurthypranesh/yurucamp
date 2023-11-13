import random

import pytest
import requests

from yurucamp.settings import env


# add one fixture for signing up a user
@pytest.fixture(scope="function")
def setup_user_account():
    rand = random.choices("0123456789", k=4)
    username = f"test-{''.join(rand)}@test.com"
    passwd = username

    response = requests.post(
        f'{env("APP_FIREBASE_AUTH_URL")}:signUp',
        params={
            "key": env("APP_FIREBASE_API_KEY"),
        },
        json={
            "email": username,
            "password": passwd,
        },
    )

    assert response is not None
    assert response.status_code == 200

    return username, passwd


# add one fixture for logging in the user
# @pytest.fixture(scope="function")
# def login_user():
#     def _login_user(username: str, password: str):
#         response = requests.post(
#             f'{env("APP_FIREBASE_AUTH_URL")}:signInWithPassword',
#             params={
#                 "key": env("APP_FIREBASE_API_KEY"),
#             },
#             json={
#                 "email": username,
#                 "password": password,
#             },
#         )
#         assert response is not None
#         assert response.status_code == 200

#         return response.json()["token"]

#     return _login_user
