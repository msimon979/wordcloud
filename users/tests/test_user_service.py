import mock
import pytest
from django.forms.models import model_to_dict

from quotes.quote_service import QuoteService
from quotes.tests.factories.quote_factories import QuoteFactory
from states.tests.factories.state_factory import StateFactory
from users.tests.factories.user_factory import UserFactory, UserInformationFactory
from users.user_service import UserService


@pytest.mark.django_db
def test_create_user_information():
    """Test user information is created"""
    user = UserFactory()
    context = {
        "state": "CA",
        "has_pet": True,
        "include_flood_coverage": True,
        "coverage_type": "basic",
    }
    user_information = UserService.create_user_information(user, context)

    assert user_information.state == "CA"
    assert user_information.has_pet is True
    assert user_information.include_flood_coverage is True
    assert user_information.coverage_type == "basic"


@pytest.mark.django_db
def test_update_user_information():
    """Test user information is updated"""
    user = UserFactory()
    user_information = UserInformationFactory(
        user=user,
        state="TX",
        has_pet=False,
        include_flood_coverage=False,
        coverage_type="premium",
    )

    context = {
        "state": "CA",
        "has_pet": True,
        "include_flood_coverage": True,
        "coverage_type": "basic",
    }

    user_information = UserService.update_user_information(user, context)

    assert user_information.state == "CA"
    assert user_information.has_pet is True
    assert user_information.include_flood_coverage is True
    assert user_information.coverage_type == "basic"


@pytest.mark.django_db
def test_get_user_state():
    """Test service returns the correct state"""
    user = UserFactory()
    UserInformationFactory(user=user, state="TX")
    assert UserService.get_user_state(user) == "TX"


@pytest.mark.django_db
def test_get_user_information():
    """Test user has information in the correct format"""
    user = UserFactory()
    UserInformationFactory(
        user=user,
        state="TX",
        has_pet=False,
        include_flood_coverage=False,
        coverage_type="premium",
    )
    assert UserService.get_user_information(user) == {
        "state": "TX",
        "has_pet": False,
        "include_flood_coverage": False,
        "coverage_type": "premium",
    }
