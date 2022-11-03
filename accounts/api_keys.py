from rest_framework_api_key.models import APIKey
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

User = get_user_model()


class NewKey:

    @classmethod
    def generate(cls, user_id):
        api_key, key = APIKey.objects.create_key(name=user_id)
        api_key.expiry_date = datetime.now() + timedelta(days=30)
        cls.add_to_user(user_id, api_key)
        return (api_key, key)

    @classmethod
    def reset(cls, user_id):
        user_key = User.get_user(user_id).api_key
        old_api_key = APIKey.objects.get(name=user_key.name)
        old_api_key.delete()
        return cls.generate(user_id)

    def add_to_user(user_id, api_key):
        user = User.get_user(user_id)
        user.api_key = api_key
        user.save()

