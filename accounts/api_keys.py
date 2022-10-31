from calendar import month
from rest_framework_api_key.models import APIKey
from datetime import datetime, timedelta


class NewKey:

    @classmethod
    def generate(cls, user_id):
        expiry_date = None
        try:
            api_key = APIKey.objects.get(name=user_id)
            if api_key.has_expired:
                expiry_date = datetime.now() + timedelta(days=30)
            else:
                expiry_date = api_key.expiry_date
            api_key.delete()

        except APIKey.DoesNotExist:
            expiry_date = datetime.now() + timedelta(days=30)

        finally:
            api_key, key = APIKey.objects.create_key(name=user_id)
            api_key.expiry_date = expiry_date
            api_key.save()
        return (key, api_key.expiry_date)
