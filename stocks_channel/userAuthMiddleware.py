from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from urllib.parse import parse_qs
from rest_framework_simplejwt.tokens import AccessToken, TokenError

User = get_user_model()


@database_sync_to_async
def get_user(id):
    try:
        return User.objects.get(id=id)
    except User.DoesNotExist:
        return AnonymousUser()


class UserAuthMiddleware:

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        parsed_query_string = parse_qs(scope["query_string"])
        try:
            token = parsed_query_string.get(b"token")[0].decode('utf-8')
            access_token = AccessToken(token)
            scope["user"] = await get_user(access_token["user_id"])
        except Exception as e:
            scope["user"] = AnonymousUser()

        return await self.app(scope, receive, send)
