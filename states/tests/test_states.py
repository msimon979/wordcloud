
import pytest
from states.tests.factories.state_factory import StateFactory
from users.tests.factories.user_factory import UserFactory

from rest_framework.test import force_authenticate
from django.urls import reverse
from rest_framework.test import APITestCase

from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
class CompanyModelsTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory(is_staff=True)

        jwt_fetch_data = {
            'username': self.user.username,
            'password': 123
        }

        url = reverse('token_obtain_pair')
        response = self.client.post(url, jwt_fetch_data, format='json')
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_get_state(self):
        state = StateFactory(state="CO", flood_cost_percentage=.5, monthly_tax=.01)
    
        url = reverse('state_details',  kwargs={'state_id': state.id})
        response = self.client.get(url)

        data = response.json()
        
        assert data["state"] == "CO"
        assert data["flood_cost_percentage"] == "0.500"
        assert data["monthly_tax"] == "0.010"
