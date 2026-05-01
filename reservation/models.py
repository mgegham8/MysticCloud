from django.db import models
from django.conf import settings
from django.utils import timezone


class Table(models.Model):
    """
    Represents a physical table in the restaurant/hookah lounge.
    """
    TABLE_TYPES = [
        ('standard', 'Standard'),
        ('vip', 'VIP / Privat Cupe'),
    ]

    table_number = models.PositiveIntegerField(unique=True)
    capacity = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    table_type = models.CharField(
        max_length=20,
        choices=TABLE_TYPES,
        default='standard'
    )

    class Meta:
        verbose_name = "Table"
        verbose_name_plural = "Tables"

    def __str__(self):
        return f"Table {self.table_number} ({self.get_table_type_display()} - {self.capacity} seats)"


class Reservation(models.Model):
    """
    Stores reservation details including customer info and table assignment.
    """
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    number_of_persons = models.PositiveIntegerField()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        related_name='reservations'
    )

    # This field allows filtering by specific date in your view
    start_date = models.DateTimeField(default=timezone.now)

    # This flag is used in your view to filter active bookings
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"
        ordering = ['-start_date']

    def save(self, *args, **kwargs):
        """
        Custom save method to handle table availability logic.
        """
        # When a new active reservation is created for today, we mark the table
        if self.is_active and self.start_date.date() == timezone.now().date():
            self.table.is_available = False
            self.table.save()
        super().save(*args, **kwargs)

    def finish_reservation(self):
        """
        Marks the reservation as completed and frees the table.
        """
        self.is_active = False
        self.save()
        self.table.is_available = True
        self.table.save()

    def __str__(self):
        return f"Reservation for {self.name} - Table {self.table.table_number} on {self.start_date.date()}"