import factory
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("email")
    password = make_password("123")
    is_staff = True
    is_superuser = True
