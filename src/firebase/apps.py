# django
from django.apps import AppConfig


class FirebaseConfig(AppConfig):
    name = 'firebase'

    def ready(self) -> None:
        # local
        from .firebase_app import firebase_app  # noqa
