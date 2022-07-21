from django.apps import AppConfig


class StocksV1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stocks_v1'

    def ready(self):
        from clock import start
        # print("Hello, stocks_v1 ready")
        start()
