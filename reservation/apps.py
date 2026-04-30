from django.apps import AppConfig

class ReservationConfig(AppConfig):
    """
    Configuration class for the Reservation application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reservation'
    verbose_name = 'Table Reservation Management'