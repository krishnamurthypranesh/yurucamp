from authn import models
from django.test import Client, TestCase
from django.urls import reverse

from yurucamp.settings import env


class TestCreateUserSession(TestCase):
    def setUp(self):
        pass

    def test_raises_400_if_body_is_not_correct_json(self):
        assert 1 == 0

    def test_returns_401_if_authentication_fails(self):
        assert 1 == 0

    def test_returns_correct_session_id_on_successful_authentication(self):
        assert 1 == 0
