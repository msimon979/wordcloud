import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from states.models import State
from states.tests.factories.state_factory import StateFactory
from users.tests.factories.user_factory import UserFactory


@pytest.mark.django_db
class InternalStateTests(APITestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True)

        jwt_fetch_data = {"username": self.user.username, "password": 123}

        url = reverse("token_obtain_pair")
        response = self.client.post(url, jwt_fetch_data, format="json")
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_get_state(self):
        """
        Given: An authenticated internal user

        When: They pull a specific state (created in fixture file)

        Then: The state information is returned
        """
        state = State.objects.get(state="CA")

        url = reverse("state_details", kwargs={"state_id": state.id})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        data = response.json()

        assert data["state"] == state.state
        assert data["flood_cost_percentage"] == str(state.flood_cost_percentage)
        assert data["monthly_tax"] == str(state.monthly_tax)

    def test_get_state_that_does_not_exist(self):
        """
        Given: An authenticated internal user

        When: They pull a specific state that does not exist

        Then: An error is returned
        """
        url = reverse("state_details", kwargs={"state_id": 4})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_patch_state(self):
        """
        Given: An authenticated internal user

        When: They patch a state object

        Then: The state is updated
        """

        state = StateFactory()

        url = reverse("state_details", kwargs={"state_id": state.id})
        data = {"flood_cost_percentage": 0.9, "monthly_tax": 0.8}

        response = self.client.patch(url, data=data)
        assert response.status_code == status.HTTP_200_OK

        data = response.json()

        state.refresh_from_db()
        assert data["state"] == state.state
        assert data["flood_cost_percentage"] == str(state.flood_cost_percentage)
        assert data["monthly_tax"] == str(state.monthly_tax)

    def test_patch_state_that_does_not_exist(self):
        """
        Given: An authenticated internal user

        When: They patch a state that does not exist

        Then: An error is returned
        """

        url = reverse("state_details", kwargs={"state_id": 99})
        data = {"flood_cost_percentage": 0.9, "monthly_tax": 0.8}

        response = self.client.patch(url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_patch_state_with_out_proper_data_returns_error(self):
        """
        Given: An authenticated internal user

        When: They patch a state with the wrong values

        Then: An error is returned
        """

        url = reverse("state_details", kwargs={"state_id": 1})
        # Needs to be a decimal
        data = {
            "flood_cost_percentage": "a",
        }

        response = self.client.patch(url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class ExternalStateTests(APITestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=False)

        jwt_fetch_data = {"username": self.user.username, "password": 123}

        url = reverse("token_obtain_pair")
        response = self.client.post(url, jwt_fetch_data, format="json")
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_patch_state_with_external_user(self):
        """
        Given: An authenticated external user

        When: They patch a state

        Then: An error is returned
        """

        url = reverse("state_details", kwargs={"state_id": 1})
        data = {
            "flood_cost_percentage": 0.9,
        }

        response = self.client.patch(url, data=data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_state_with_external_user(self):
        """
        Given: An authenticated external user

        When: They get a state

        Then: An error is returned
        """

        url = reverse("state_details", kwargs={"state_id": 1})

        response = self.client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
