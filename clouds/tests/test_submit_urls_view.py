from django.urls import reverse
from rest_framework.test import APITestCase


class TestSubmitUrlView(APITestCase):
    def test_successful_url(self):
        """
        Given: A payload to the submit url

        When: The url is deemed valid

        Then: Create the object and return a 202
        """
        url = reverse("submit_url")
        resp = self.client.post(
            url, data={"url": "https://en.wikipedia.org/wiki/Basketball"}
        )
        assert resp.status_code == 202

    def test_failed_url(self):
        """
        Given: a payload to the submit url

        When: The url is invalid

        Then: Return an error
        """
        url = reverse("submit_url")
        resp = self.client.post(url, data={"url": "en.wikipedia.org/wiki/Basketball"})

        assert resp.status_code == 400
        assert resp.json()["error"] == "invalid url: en.wikipedia.org/wiki/Basketball"

    def test_missing_url_in_payload(self):
        """
        Given: a payload to the submit url

        When: There is no url

        Then: Return an error
        """
        url = reverse("submit_url")
        resp = self.client.post(url)

        assert resp.status_code == 400
        assert resp.json()["error"] == "missing url in data"
