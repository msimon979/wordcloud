import factory
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from users.models import UserInformation


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("email")
    password = make_password("123")
    is_staff = True
    is_superuser = True


class UserInformationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserInformation

    state = "VA"
    has_pet = True
    coverage_type = "basic"
    include_flood_coverage = True
