import mock
import pytest
from django.forms.models import model_to_dict

from quotes.quote_service import QuoteService
from quotes.tests.factories.quote_factories import QuoteFactory
from states.tests.factories.state_factory import StateFactory


@pytest.mark.django_db
def test_get_user_quotes():
    quote = QuoteFactory(state="CO", user_id=2)
    assert QuoteService.get_user_quotes(quote.user_id) == [model_to_dict(quote)]


@mock.patch("lib.cost_calculator.CostCalculator.update_quote")
@pytest.mark.django_db
def test_update_existing_quotes_is_called(mock_cost_calc):
    quote = QuoteFactory()
    state = StateFactory()

    QuoteService.update_existing_quote(quote, state)
    mock_cost_calc.assert_called_with(quote, state)
