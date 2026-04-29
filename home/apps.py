from django.apps import AppConfig


class HomeConfig(AppConfig):
    """
    Configuration class for the 'home' application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

    # This name will appear in the Django Admin sidebar
    verbose_name = 'Site Content Management'