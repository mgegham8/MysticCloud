from django.apps import AppConfig


class UserConfig(AppConfig):
    """
    Configuration class for the 'users' application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        """
        This method is called when the application is fully loaded.
        We import the signals here to ensure they are registered
        and active as soon as the server starts.
        """
        import users.signals