from django.apps import AppConfig


class NaWebappConfig(AppConfig):
    name = 'NA_WebApp'

    def ready(self):
        import NA_WebApp.signals
