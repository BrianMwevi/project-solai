from django.apps import AppConfig
from clock import start


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        from clock import start
        start()
