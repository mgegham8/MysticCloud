from django.db import models

class OrderStatus(models.TextChoices):
    """
    Defines status options for orders or reservations.
    """
    PENDING = 'P', 'Pending'
    CONFIRMED = 'C', 'Confirmed'
    CANCELLED = 'X', 'Cancelled'
    COMPLETED = 'D', 'Delivered'

class UserRole(models.TextChoices):
    """
    Defines user roles within the system.
    """
    ADMIN = 'AD', 'Administrator'
    CHEF = 'CH', 'Chef'
    CUSTOMER = 'CU', 'Customer'