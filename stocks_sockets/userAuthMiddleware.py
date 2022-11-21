from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from channels.db import database_sync_to_async
from urllib.parse import parse_qs
from rest_framework_api_key.models import APIKey

User = get_user_model()


@database_sync_to_async
def get_user(key):

    if not APIKey.objects.is_valid(key):
        return AnonymousUser()
    try:
        api_key = APIKey.objects.get_from_key(key)
        user = User.objects.get(api_key=api_key)
        return user
    except (User.DoesNotExist, APIKey.DoesNotExist):
        return AnonymousUser()


class UserAuthMiddleware:

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        parsed_query_string = parse_qs(scope["query_string"])
        try:
            key = parsed_query_string.get(b"api_key")[0].decode('utf-8')
            scope["user"] = await get_user(key)
        except Exception as e:
            scope["user"] = AnonymousUser()

        return await self.app(scope, receive, send)
