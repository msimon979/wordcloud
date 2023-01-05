import decimal

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lib.cost_calculator import CostCalculator, format_float, get_costs
from quotes.models import Quote
from states.models import State
from states.tests.factories.state_factory import StateFactory
from users.tests.factories.user_factory import UserFactory, UserInformationFactory


@pytest.mark.django_db
class InternalUserTests(APITestCase):
    def setUp(self):
        """Auth the client with internal user"""
        self.user = UserFactory(is_staff=True)

        jwt_fetch_data = {"username": self.user.username, "password": 123}

        url = reverse("token_obtain_pair")
        response = self.client.post(url, jwt_fetch_data, format="json")
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_post_user(self):
        """
        Given: An authenticated internal user

        When: They create a user

        Then: The user is created successfully
        """
        url = reverse("users")
        data = {
            "password": 123,
            "state": "CA",
            "has_pet": True,
            "include_flood_coverage": True,
            "coverage_type": "basic",
            "username": "sure_thing",
            "email": "sure_thing@gmail.com",
            "first_name": "test",
            "last_name": "test",
        }

        response = self.client.post(url, data=data)
        assert response.status_code == status.HTTP_201_CREATED

        data = response.json()

    def test_get_users(self):
        """
        Given: An authenticated internal user

        When: They request users

        Then: The user information is returned
        """
        user_1 = UserFactory(is_staff=False, username="test", email="test@gmail.com")
        user_2 = UserFactory(is_staff=False, username="test2", email="test2@gmail.com")

        UserInformationFactory(user_id=user_1.id, state="CA")
        UserInformationFactory(user_id=user_2.id, state="CA")

        url = reverse("users")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2

        response_user_ids = [d["id"] for d in data]

        assert user_1.id in response_user_ids
        assert user_2.id in response_user_ids

    def test_get_user(self):
        """
        Given: An authenticated internal user

        When: They request a user

        Then: The user is returned
        """
        url = reverse("user_details", kwargs={"user_id": self.user.id})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_get_user_that_does_not_exist(self):
        """
        Given: An authenticated internal user

        When: They request a user that does not exist

        Then: An error is returned
        """
        url = reverse("user_details", kwargs={"user_id": 99})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_patch_user(self):
        """
        Given: An authenticated internal user

        When: They patch a user

        Then: The user is patched
        """
        user = UserFactory()
        UserInformationFactory(user=user, state="CA")
        url = reverse("user_details", kwargs={"user_id": user.id})
        data = {"first_name": "TEST_NAME", "state": "TX"}

        response = self.client.patch(url, data=data)
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["quotes"][0]["state"] == "TX"
        assert data["first_name"] == "TEST_NAME"

    def test_patch_a_user_that_does_not_exist(self):
        """
        Given: An authenticated internal user

        When: They patch a user that does not exist

        Then: An error is returned
        """
        url = reverse("user_details", kwargs={"user_id": 99})
        data = {"first_name": "TEST_NAME", "state": "TX"}

        response = self.client.patch(url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class ExternalUserTests(APITestCase):
    def setUp(self):
        """Auth the client with internal user"""
        self.user = UserFactory(is_staff=False)

        jwt_fetch_data = {"username": self.user.username, "password": 123}

        url = reverse("token_obtain_pair")
        response = self.client.post(url, jwt_fetch_data, format="json")
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_post_user(self):
        """
        Given: An authenticated external user

        When: They create a user

        Then: They get an error
        """
        url = reverse("users")
        data = {
            "password": 123,
            "state": "CA",
            "has_pet": True,
            "include_flood_coverage": True,
            "coverage_type": "basic",
            "username": "sure_thing",
            "email": "sure_thing@gmail.com",
            "first_name": "test",
            "last_name": "test",
        }

        response = self.client.post(url, data=data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_users(self):
        """
        Given: An authenticated external user

        When: They request users

        Then: They get an error
        """
        user_1 = UserFactory(is_staff=False, username="test", email="test@gmail.com")
        user_2 = UserFactory(is_staff=False, username="test2", email="test2@gmail.com")

        UserInformationFactory(user_id=user_1.id, state="CA")
        UserInformationFactory(user_id=user_2.id, state="CA")

        url = reverse("users")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_user(self):
        """
        Given: An authenticated external user

        When: They request their user

        Then: The user is returned
        """
        url = reverse("user_details", kwargs={"user_id": self.user.id})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_get_user_that_is_not_their_own(self):
        """
        Given: An authenticated external user

        When: They request a user that is not their own

        Then: An error is returned
        """
        user = UserFactory()
        url = reverse("user_details", kwargs={"user_id": user.id})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_patch_user(self):
        """
        Given: An authenticated external user

        When: They patch their user

        Then: The user is patched
        """
        user = UserFactory()
        UserInformationFactory(user=self.user, state="CA")
        url = reverse("user_details", kwargs={"user_id": self.user.id})
        data = {"first_name": "TEST_NAME", "state": "TX"}

        response = self.client.patch(url, data=data)
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["quotes"][0]["state"] == "TX"
        assert data["first_name"] == "TEST_NAME"

    def test_patch_a_user_that_does_not_belong_to_them(self):
        """
        Given: An authenticated external user

        When: They patch another user

        Then: An error is returned
        """
        user = UserFactory()
        url = reverse("user_details", kwargs={"user_id": user.id})
        data = {"first_name": "TEST_NAME", "state": "TX"}

        response = self.client.patch(url, data=data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
