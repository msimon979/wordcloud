from quotes.models import Quote
from states.models import State

BASIC_COST = 20
PREMIUM_COST = 40
PET_COST = 20

COVERAGE_COSTS = {
    "basic": BASIC_COST,
    "premium": PREMIUM_COST,
}


class CostCalculator:
    @staticmethod
    def create_quote(user_information):
        state_costs = State.objects.get(state=user_information.state)

        coverage_cost = COVERAGE_COSTS.get(user_information.coverage_type)
        has_pet = PET_COST if user_information.has_pet else 0

        total_before_state_costs = coverage_cost + has_pet

        monthly_tax_cost = state_costs.monthly_tax * total_before_state_costs
        flood_cost = state_costs.flood_cost_percentage * total_before_state_costs

        query_args = {
            "full_name": f"{user_information.user.first_name} {user_information.user.last_name}",
            "coverage_type": user_information.coverage_type,
            "state": user_information.state,
            "has_pet": user_information.has_pet,
            "include_flood_coverage": user_information.include_flood_coverage,
            "monthly_subtotal": total_before_state_costs + flood_cost,
            "monthly_taxes": monthly_tax_cost,
            "monthly_total": total_before_state_costs + flood_cost + monthly_tax_cost,
            "user_id": user_information.user.id,
        }

        Quote.objects.create(**query_args)
