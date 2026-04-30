from django.contrib import admin
from reservation.models import Reservation, Table


class TableAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing restaurant tables.
    """
    list_display = ("table_number", "capacity")
    list_filter = ("capacity",)
    search_fields = ("table_number",)
    ordering = ("table_number",)


class ReservationAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing customer reservations.
    """
    list_display = ("name", "table", "start_date", "end_time", "phone", "number_of_persons")
    list_filter = ("start_date", "table", "number_of_persons")
    search_fields = ("name", "phone", "email")
    date_hierarchy = "start_date"  # Adds a date navigation bar at the top
    ordering = ("-start_date",)

    # Grouping fields into sections for better organization
    fieldsets = (
        ("CUSTOMER INFO", {
            "fields": ("name", "email", "phone", "user")
        }),
        ("RESERVATION DETAILS", {
            "fields": ("table", "number_of_persons", ("start_date", "end_time"))
        }),
    )


# Registering models with their respective Admin classes
# These should be the ONLY registration lines in this file
admin.site.register(Table, TableAdmin)
admin.site.register(Reservation, ReservationAdmin)