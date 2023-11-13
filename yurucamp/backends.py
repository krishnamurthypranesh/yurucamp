import requests

from exc import IncorrectAuthenticationCredentialsException
from authn.models import User
from yurucamp.settings import env


class FirebaseAuthenticationBackend(object):
    def __init__(self):
        print(dir(env))
        self._backend = self.__FirebaseAuthenticationBackend(
            url_prefix=env("APP_FIREBASE_AUTH_URL"),
            api_key=env("APP_FIREBASE_API_KEY"),
        )

    class __FirebaseAuthenticationBackend:
        def __init__(self, api_key: str, url_prefix: str):
            self.api_key = api_key
            self.url_prefix = url_prefix

        def user_sign_in(self, username: str, password: str):
            payload = {
                "email": username,
                "password": password,
            }

            print(f"payload: {payload}")

            endpoint = "signInWithPassword"

            response = requests.post(
                url=f"{self.url_prefix}:{endpoint}",
                params={"key": self.api_key},
                json=payload,
                headers={"Content-Type": "application/json"},
            )

            if response.status_code == 400:
                raise IncorrectAuthenticationCredentialsException()
            else:
                response.raise_for_status()

            return response.json()

    def authenticate(self, request, username, password):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            print(f"user: {username} does not exist")
            return

        self._backend.user_sign_in(username=username, password=password)

        return user

    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
            return user
        except User.DoesNotExist:
            return None
