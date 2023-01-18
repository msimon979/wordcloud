from django.urls import reverse
from rest_framework.test import APITestCase

from clouds.models import Words
from clouds.views import DEFAULT_LIMIT


class TestWordsView(APITestCase):

    # Create factory if you have time
    def create_words(self):
        Words.objects.create(word="basketball", count=200)
        Words.objects.create(word="soccer", count=100)
        Words.objects.create(word="baseball", count=50)
        Words.objects.create(word="swimming", count=20)
        Words.objects.create(word="tennis", count=10)

    def test_successful_get_data(self):
        """
        Given: A request for top words

        When: The data is returned

        Then: It returns in desc ordering
        """
        self.create_words()

        url = reverse("get_words")

        resp = self.client.get(url)
        assert resp.status_code == 200

        results = resp.json()["results"]
        assert len(results) == DEFAULT_LIMIT

        expected_structure = [
            {"word": "basketball", "count": 200},
            {"word": "soccer", "count": 100},
            {"word": "baseball", "count": 50},
        ]

        assert expected_structure == results

    def test_successful_get_data_with_limit(self):
        """
        Given: A request for top words

        When: A limit query param is provided

        Then: Return the limit
        """
        limit = 2

        self.create_words()

        url = reverse("get_words") + f"?limit={limit}"

        resp = self.client.get(url)
        assert resp.status_code == 200

        results = resp.json()["results"]
        assert len(results) == limit

        expected_structure = [
            {"word": "basketball", "count": 200},
            {"word": "soccer", "count": 100},
        ]

        assert expected_structure == results

    def test_successful_get_data_while_ignoring_limit(self):
        """
        Given: A request for top words

        When: The limit exceeds MAX_LIMIT

        Then: Return DEFAULT_LIMIT
        """
        limit = 21

        self.create_words()

        url = reverse("get_words") + f"?limit={limit}"

        resp = self.client.get(url)
        assert resp.status_code == 200

        results = resp.json()["results"]
        assert len(results) == DEFAULT_LIMIT

        expected_structure = [
            {"word": "basketball", "count": 200},
            {"word": "soccer", "count": 100},
            {"word": "baseball", "count": 50},
        ]

        assert expected_structure == results
