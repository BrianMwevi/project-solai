from calendar import month
from rest_framework_api_key.models import APIKey
from datetime import datetime, timedelta


class NewKey:

    def generate(user_id):
        api_key, key = APIKey.objects.create_key(name=user_id)
        api_key.expiry_date = datetime.now() + timedelta(days=30)
        api_key.save()
        return key
