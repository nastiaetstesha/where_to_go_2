from django.apps import AppConfig
import os


class PlacesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'places'
    path = os.path.dirname(os.path.abspath(__file__))
