from django.contrib import admin
from .models import User, Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the User model.
    """
    # Columns to display in the list view
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')

    # Fields to search by in the admin search bar
    search_fields = ('email', 'first_name', 'last_name')

    # Filter options in the right sidebar
    list_filter = ('is_active', 'is_staff')

    # Default ordering
    ordering = ('email',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Profile model.
    """
    # Columns to display
    list_display = ('user', 'country', 'phone_field')

    # Enable search by user's email or names (linked via ForeignKey)
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'country')