import json

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from rest_framework_api_key.models import APIKey

from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class StockCrudTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.stock = {
            "ticker": "ABSA",
            "price": 11.6,
            "open": 11.6,
            "change": 0.0,
            "high": 11.6,
            "low": 11.6
        }

    def test_can_create_stocks(self):
        api_key = "tPch8sqr.25esNION0ZxmJqCOh0xYr6kY1NTPfzul"
        # headers = {"Authorization": f"Api-Key {api_key}"}
        self.client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
        response = self.client.post(
            reverse("realtime"), data={"stocks": [self.stock]})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
