import factory

from states.models import State


class StateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = State

    state = "CO"
    flood_cost_percentage = 0.5
    monthly_tax = 0.01
