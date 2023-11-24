from authn import models
from django.test import Client, TestCase
from django.urls import reverse

from yurucamp.settings import env


class TestFirebaseAuthenticationBackend(TestCase):
    def setUp(self):
        pass

    def test_makes_correct_request_when_authenticating_users(self):
        assert 1 == 0

    def test_raises_correct_error_when_firebase_returns_400(self):
        assert 1 == 0

    def test_raises_correct_error_when_firebase_returns_non_200_response(self):
        assert 1 == 0

    def test_returns_401_if_user_does_not_exist(self):
        assert 1 == 0

    def test_returns_correct_user_object_if_authentication_works(self):
        assert 1 == 0
