import json
import base64

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from django.contrib.auth import get_user_model


PASSWORD = 'pAsswOrd!'


def create_user(email='user@gmail.com', password=PASSWORD):
    user = get_user_model().objects.create_user(
        email=email,
        first_name='Test',
        last_name='User',
        password=password
    )
    # bypassing email confirmation
    user.is_active = True
    user.save()
    return user


class AuthenticationTest(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_user_can_sign_up(self):
        response = self.client.post(reverse('signup'), data={
            'email': 'user@gmail.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': PASSWORD,
            'password2': PASSWORD,
            'usage': 'PERSONAL',
            'role': 'DEVELOPER',
        })
        user = get_user_model().objects.last()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], str(user.id))
        self.assertEqual(response.data['email'], user.email)
        self.assertEqual(response.data['first_name'], user.first_name)
        self.assertEqual(response.data['last_name'], user.last_name)
        self.assertEqual(response.data['usage'], user.usage)
        self.assertEqual(response.data['role'], user.role)

    def test_user_can_login(self):
        user = create_user()

        response = self.client.post(reverse('login'), data={
            'email': user.email,
            'password': PASSWORD,
        })

        access = response.data['access']
        header, payload, signature = access.split('.')
        # == adding back padding chars that JWT strips out to avoid errors
        decoded_payload = base64.b64decode(f'{payload}==')
        payload_data = json.loads(decoded_payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['refresh'])
        self.assertEqual(payload_data['id'], str(user.id))
        self.assertEqual(payload_data['email'], str(user.email))
        self.assertEqual(payload_data['first_name'], str(user.first_name))
        self.assertEqual(payload_data['first_name'], str(user.first_name))
        self.assertEqual(payload_data['last_name'], str(user.last_name))

    def test_change_password(self):
        user = create_user()
        login_response = self.client.post(reverse('login'), data={
            'email': user.email,
            'password': PASSWORD,
        })

        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        password_response = self.client.put(reverse('change_password'), data={
            'old_password': PASSWORD,
            'new_password': "pass11234"
        })
        updated_user = get_user_model().objects.get(email=user.email)

        self.assertEqual(password_response.status_code, status.HTTP_200_OK)
        self.assertTrue(updated_user.check_password('pass11234'))
