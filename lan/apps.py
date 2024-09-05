from django.apps import AppConfig


class LanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lan'

    # def ready(self):
    #     from .cron2 import start
    #     start()