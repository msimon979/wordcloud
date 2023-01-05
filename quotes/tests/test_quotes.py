import mock
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from quotes.helpers import get_quote, update_quote
from quotes.tests.factories.quote_factories import QuoteFactory
from states.tests.factories.state_factory import StateFactory
from users.tests.factories.user_factory import UserFactory


@pytest.mark.django_db
def test_get_quote_returns_quote():
    """Test get_quote returns quote"""
    quote = QuoteFactory()
    assert get_quote(quote.id) == quote


@pytest.mark.django_db
def test_get_quote_returns_none():
    """Test None is returned for a quote that does not exist"""
    assert get_quote(1) is None


@mock.patch("quotes.quote_service.QuoteService.update_existing_quote")
@pytest.mark.django_db
def test_update_quote_calls_quote_service(mock_quote_service):
    """
    Given: A quote

    When: The state the quote is in gets updated
    AND update_quote gets called

    Then: The QuoteService gets called
    """
    state = StateFactory()
    quote = QuoteFactory(state=state.state)

    state.flood_cost_percentage = 0.1
    state.save()

    update_quote(quote)
    mock_quote_service.assert_called_with(quote, state)


@mock.patch("quotes.quote_service.QuoteService.update_existing_quote")
@pytest.mark.django_db
def test_update_quote_does_not_call_quote_service(mock_quote_service):
    """
    Given: A quote

    When: update_quote gets called

    Then: Then the QuoteService is not called
    """
    state = StateFactory()
    quote = QuoteFactory(state=state.state)

    update_quote(quote)
    mock_quote_service.assert_not_called()


@pytest.mark.django_db
class InternalQuoteTests(APITestCase):
    def setUp(self):
        """Auth the client with internal user"""
        self.user = UserFactory(is_staff=True)

        jwt_fetch_data = {"username": self.user.username, "password": 123}

        url = reverse("token_obtain_pair")
        response = self.client.post(url, jwt_fetch_data, format="json")
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_get_quote(self):
        """
        Given: An internal user

        When: They make a request for a quote

        Then: The quote is returned
        """
        quote = QuoteFactory()
        url = reverse("quote_details", kwargs={"quote_id": quote.id})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        data = response.json()

        assert data["full_name"] == quote.full_name
        assert data["coverage_type"] == quote.coverage_type
        assert data["state"] == quote.state
        assert data["has_pet"] == quote.has_pet
        assert data["include_flood_coverage"] == quote.include_flood_coverage
        assert data["monthly_subtotal"] == quote.monthly_subtotal
        assert data["monthly_taxes"] == quote.monthly_taxes
        assert data["monthly_total"] == quote.monthly_total
        assert data["user_id"] == quote.user_id

    def test_get_quote_that_doesnt_exist(self):
        """
        Given: An internal user

        When: They make a request for a quote that does not exist

        Then: Then an error is returned
        """
        url = reverse("quote_details", kwargs={"quote_id": 99})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class ExternalQuoteTests(APITestCase):
    def setUp(self):
        """Auth the client with external user"""
        self.user = UserFactory(is_staff=False)

        jwt_fetch_data = {"username": self.user.username, "password": 123}

        url = reverse("token_obtain_pair")
        response = self.client.post(url, jwt_fetch_data, format="json")
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_get_quote(self):
        """
        Given: An external user with a quote

        When: They make a request for the quote

        Then: The quote is returned
        """
        state = StateFactory()
        quote = QuoteFactory(user_id=self.user.id, state=state.state)
        url = reverse("quote_details", kwargs={"quote_id": quote.id})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        data = response.json()

        assert data["full_name"] == quote.full_name
        assert data["coverage_type"] == quote.coverage_type
        assert data["state"] == quote.state
        assert data["has_pet"] == quote.has_pet
        assert data["include_flood_coverage"] == quote.include_flood_coverage
        assert data["monthly_subtotal"] == quote.monthly_subtotal
        assert data["monthly_taxes"] == quote.monthly_taxes
        assert data["monthly_total"] == quote.monthly_total
        assert data["user_id"] == quote.user_id

    def test_get_quote_that_does_not_belong_to_the_user(self):
        """
        Given: An external user without a quote

        When: They make a request for someone elses quote

        Then: A 401 status code is returned
        """
        state = StateFactory()
        quote = QuoteFactory(user_id=99, state=state.state)
        url = reverse("quote_details", kwargs={"quote_id": quote.id})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_quote_that_doesnt_exist(self):
        """
        Given: An external user

        When: They make a request for a quote that does not exist

        Then: Then an error is returned
        """
        url = reverse("quote_details", kwargs={"quote_id": 99})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
