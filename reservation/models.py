from django.db import models
from django.conf import settings  # Use settings.AUTH_USER_MODEL for better practice


class Table(models.Model):
    """
    Represents a physical table in the restaurant.
    """
    table_number = models.PositiveIntegerField(unique=True)
    capacity = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Table"
        verbose_name_plural = "Tables"

    def __str__(self):
        return f"Table {self.table_number} (Capacity: {self.capacity})"


class Reservation(models.Model):
    """
    Stores reservation details including customer info and assigned table.
    """
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20)  # Changed to CharField for phone numbers
    number_of_persons = models.PositiveIntegerField()

    # Using AUTH_USER_MODEL is more flexible
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        related_name='reservations'  # Changed related_name to be more natural
    )

    start_date = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"
        ordering = ['-start_date']

    def cancel_reservation(self):
        """
        Deletes the reservation instance.
        """
        self.delete()

    def __str__(self):
        return f"Reservation for {self.name} on {self.start_date.strftime('%Y-%m-%d %H:%M')}"