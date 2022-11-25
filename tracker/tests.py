from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from accounts.tests import create_user
from rest_framework import status
from stocks_v1.models import Stock


PASSWORD = 'pAsswOrd!'


def create_stock():
    data = {
        "ticker": "SCOM",
        "price": 24,
        "open": 25,
        "change": 0.4,
    }
    return Stock.objects.create(**data)


class TestStockTracking(APITestCase):

    def setUp(self):

        self.client = APIClient()
        self.user = create_user()
        self.stock = create_stock()

        login_response = self.client.post(reverse('login'), data={
            'email': self.user.email,
            'password': PASSWORD,
        })

        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def test_can_create_tracker(self):
        create_response = self.client.post(reverse('tracker-list'), data={
            "stock": self.stock.id,
            "quote_price": 24
        })

        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(create_response.data["id"], 1)

    def test_can_get_tracker(self):
        create_response = self.client.post(reverse('tracker-list'), data={
            "stock": self.stock.id,
            "quote_price": 24
        })
        tracker_id = create_response.data["id"]
        get_response = self.client.get(
            reverse('tracker-detail', kwargs={"pk": tracker_id}))

        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    def test_can_update_tracker(self):
        create_response = self.client.post(reverse('tracker-list'), data={
            "stock": self.stock.id,
            "quote_price": 24
        })
        tracker_id = create_response.data["id"]
        update_response = self.client.patch(
            reverse('tracker-detail', kwargs={"pk": tracker_id}), data={"quote_price": 25})

        self.assertEqual(float(update_response.data['quote_price']), float(25))

    def test_can_delete_tracker(self):
        create_response = self.client.post(reverse('tracker-list'), data={
            "stock": self.stock.id,
            "quote_price": 24
        })
        tracker_id = create_response.data["id"]
        delete_response = self.client.delete(
            reverse('tracker-detail', kwargs={"pk": tracker_id}))

        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
