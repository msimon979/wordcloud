import decimal

import pytest

from lib.cost_calculator import CostCalculator, format_float, get_costs
from quotes.models import Quote
from states.models import State
from states.tests.factories.state_factory import StateFactory
from users.tests.factories.user_factory import UserFactory, UserInformationFactory


@pytest.mark.django_db
def test_format_float():
    """Test format"""
    assert format_float(1.1133333333) == 1.11
    assert format_float(1.1) == 1.1
    assert format_float(1.10000) == 1.1
    assert format_float(1111.11900) == 1111.11


@pytest.mark.django_db
def test_get_costs():
    """Test get costs returns the correct information"""
    user = UserFactory(is_staff=False)
    state = StateFactory()
    user_information = UserInformationFactory(user=user, state=state.state)

    subtotal, monthly_tax_cost = get_costs(state, user_information)

    assert subtotal == 60
    assert monthly_tax_cost == 0.6


@pytest.mark.parametrize(
    "state_abbr,has_pet,include_flood_coverage,coverage_type,expected_monthly_subtotal,expected_monthly_taxes,expected_monthly_total",
    [
        ("CA", True, True, "basic", 40.80, 0.40, 41.20),
        ("CA", True, True, "premium", 61.2, 0.61, 61.81),
        ("NY", True, False, "premium", 60, 1.2, 61.2),
        ("TX", False, True, "basic", 30, 0.15, 30.15),
    ],
)
@pytest.mark.django_db
def test_quotes_from_example(
    state_abbr,
    has_pet,
    include_flood_coverage,
    coverage_type,
    expected_monthly_subtotal,
    expected_monthly_taxes,
    expected_monthly_total,
):
    """
    Acceptance tests from https://sure.notion.site/2022-Backend-Take-Home-Prompt-5fd6c44daa55421081b144778e07ff68
    """
    state = State.objects.get(state=state_abbr)
    user = UserFactory(is_staff=False)
    user_information = UserInformationFactory(
        user=user,
        state=state.state,
        has_pet=has_pet,
        include_flood_coverage=include_flood_coverage,
        coverage_type=coverage_type,
    )

    # Deleting quote here because it gets created after UserInformation
    Quote.objects.get(user_id=user.id).delete()

    quote = CostCalculator.create_quote(user_information)

    assert quote.monthly_subtotal == expected_monthly_subtotal
    assert quote.monthly_taxes == expected_monthly_taxes
    assert quote.monthly_total == expected_monthly_total


@pytest.mark.parametrize(
    "state_abbr,has_pet,include_flood_coverage,coverage_type",
    [
        (
            "CA",
            True,
            True,
            "basic",
        ),
        (
            "CA",
            True,
            True,
            "premium",
        ),
        (
            "NY",
            True,
            False,
            "premium",
        ),
        (
            "TX",
            False,
            True,
            "basic",
        ),
    ],
)
@pytest.mark.django_db
def test_there_are_no_duplicate_quotes(
    state_abbr,
    has_pet,
    include_flood_coverage,
    coverage_type,
):
    """
    Given: An existing quote

    When: A quote is created with the same information

    Then: It is not created
    """
    state = State.objects.get(state=state_abbr)
    user = UserFactory(is_staff=False)
    user_information = UserInformationFactory(
        user=user,
        state=state.state,
        has_pet=has_pet,
        include_flood_coverage=include_flood_coverage,
        coverage_type=coverage_type,
    )

    assert CostCalculator.create_quote(user_information) is None


@pytest.mark.django_db
def test_update_quote():
    """
    Given: A quote

    When: The state the quote is in has its information updated

    Then: The quote gets updated after CostCalculator.update_quote
    """
    state = State.objects.get(state="CA")
    user = UserFactory(is_staff=False)
    UserInformationFactory(
        user=user,
        state=state.state,
    )

    quote = Quote.objects.get(user_id=user.id)

    assert quote.monthly_subtotal == 40.80
    assert quote.monthly_taxes == 0.40
    assert quote.monthly_total == 41.20

    state.flood_cost_percentage = decimal.Decimal("0.090")
    state.save()
    state.refresh_from_db

    updated_quote = CostCalculator.update_quote(quote, state)

    assert updated_quote.monthly_subtotal == 43.6
    assert updated_quote.monthly_taxes == 0.43
    assert updated_quote.monthly_total == 44.03
