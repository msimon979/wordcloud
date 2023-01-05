import factory

from quotes.models import Quote


class QuoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Quote

    full_name = "test user"
    coverage_type = "basic"
    state = "VA"
    has_pet = False
    include_flood_coverage = True
    monthly_subtotal = 20
    monthly_taxes = 0.8
    monthly_total = 20.8
    user_id = 1
