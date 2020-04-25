from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from unittest import TestCase


class UserAPITests(TestCase):
    factory = APIRequestFactory()

    def test1(self):
        self.c = APIClient()
        self.c.login(username="user3", password="danil528")
        self.c.logout()

        assert True is False
