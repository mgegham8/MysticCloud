from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from reservation.models import Reservation, Table

class TableAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing restaurant tables with a direct Edit button.
    """
    # Ավելացնում ենք 'edit_button' սյունակը ցուցակում
    list_display = ("table_number", "table_type", "capacity", "is_available", "edit_button")
    list_filter = ("table_type", "capacity", "is_available")
    search_fields = ("table_number",)
    ordering = ("table_number",)

    # Ֆունկցիա, որը ստեղծում է կոդով Edit կոճակ
    def edit_button(self, obj):
        url = reverse('admin:reservation_table_change', args=[obj.pk])
        return format_html(
            '<a class="button" href="{}" style="background-color: #417690; color: white; padding: 5px 10px; border-radius: 4px; text-decoration: none;">Edit</a>',
            url
        )

    edit_button.short_description = 'Actions' # Սյունակի վերնագիրը

    # Քո նախկինում ունեցած գործողությունները (actions)
    actions = ['make_available', 'make_unavailable']

    @admin.action(description='Mark selected tables as available')
    def make_available(self, request, queryset):
        queryset.update(is_available=True)
        self.message_user(request, "Selected tables are now marked as available.")

    @admin.action(description='Mark selected tables as unavailable')
    def make_unavailable(self, request, queryset):
        queryset.update(is_available=False)
        self.message_user(request, "Selected tables are now marked as unavailable.")

# Մնացած մասը թողնում ենք նույնը
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("name", "table", "start_date", "is_active", "phone", "number_of_persons")
    list_filter = ("start_date", "table", "number_of_persons", "is_active")
    search_fields = ("name", "phone", "email")
    date_hierarchy = "start_date"
    ordering = ("-start_date",)

    fieldsets = (
        ("CUSTOMER INFO", {"fields": ("name", "email", "phone", "user")}),
        ("RESERVATION DETAILS", {"fields": ("table", "number_of_persons", "start_date", "is_active")}),
    )

admin.site.register(Table, TableAdmin)
admin.site.register(Reservation, ReservationAdmin)