from typing import Iterable, Union

from django.db import IntegrityError

from quotes.models import Quote
from states.models import State
from users.models import UserInformation

BASIC_COST = 20
PREMIUM_COST = 40
PET_COST = 20

COVERAGE_COSTS = {
    "basic": BASIC_COST,
    "premium": PREMIUM_COST,
}


def format_float(cost: float) -> float:
    num_decimals = 2
    return int(cost * 10**num_decimals) / 10**num_decimals


def get_costs(
    state: State, user_information: UserInformation
) -> Iterable[Union[bool, str]]:
    coverage_cost = COVERAGE_COSTS.get(user_information.coverage_type)
    has_pet = PET_COST if user_information.has_pet else 0

    subtotal = coverage_cost + has_pet
    if user_information.include_flood_coverage:
        subtotal = (state.flood_cost_percentage * subtotal) + subtotal

    monthly_tax_cost = state.monthly_tax * subtotal

    return subtotal, monthly_tax_cost


class CostCalculator:
    @staticmethod
    def create_quote(user_information: UserInformation) -> Quote:
        try:
            state = State.objects.get(state=user_information.state)
        except State.DoesNotExist:
            return

        subtotal, monthly_tax_cost = get_costs(state, user_information)

        query_args = {
            "full_name": f"{user_information.user.first_name} {user_information.user.last_name}",
            "coverage_type": user_information.coverage_type,
            "state": user_information.state,
            "has_pet": user_information.has_pet,
            "include_flood_coverage": user_information.include_flood_coverage,
            "monthly_subtotal": format_float(subtotal),
            "monthly_taxes": format_float(monthly_tax_cost),
            "monthly_total": format_float(subtotal + monthly_tax_cost),
            "user_id": user_information.user.id,
        }

        try:
            new_quote = Quote.objects.create(**query_args)
        except IntegrityError:
            return

        Quote.objects.filter(user_id=user_information.user.id).exclude(
            id=new_quote.id
        ).delete()

        return new_quote

    @staticmethod
    def update_quote(quote: Quote, state: State) -> Quote:
        user_information = UserInformation.objects.get(user_id=quote.user_id)

        subtotal, monthly_tax_cost = get_costs(state, user_information)

        quote.monthly_subtotal = format_float(subtotal)
        quote.monthly_taxes = format_float(monthly_tax_cost)
        quote.monthly_total = format_float(subtotal + monthly_tax_cost)

        try:
            quote.save()
            return quote
        except IntegrityError:
            return
