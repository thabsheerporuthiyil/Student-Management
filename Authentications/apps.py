from django.apps import AppConfig

class AuthenticationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Authentications'

    def ready(self):
        import Authentications.signals

