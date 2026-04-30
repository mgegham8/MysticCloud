from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile

# Get the custom user model defined in settings
User = get_user_model()

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal receiver to handle Profile creation and updates.
    Ensures that every User has an associated Profile without
    triggering duplicate key errors during tests or migrations.
    """
    if created:
        # Use get_or_create to prevent IntegrityError if a profile
        # was already instantiated elsewhere (common in testing)
        Profile.objects.get_or_create(user=instance)
    else:
        # Save the profile only if it exists to avoid AttributeErrors
        if hasattr(instance, 'profile'):
            instance.profile.save()