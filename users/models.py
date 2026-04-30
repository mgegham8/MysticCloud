from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from helpers.media_upload import upload_user_images


class UserManager(BaseUserManager):
    """
    Custom manager for User model where email is the unique identifier.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model supporting email authentication.
    """
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=155, blank=True, null=True)
    last_name = models.CharField(max_length=155, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return str(self.email)


class Profile(models.Model):
    """
    Profile model to store additional user information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to=upload_user_images, blank=True, null=True)
    country = CountryField(blank=True, null=True)
    phone_field = PhoneNumberField(blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        # Using a safer way to access the email that usually satisfies IDEs
        return f"Profile for {self.user_email}"

    @property
    def user_email(self):
        """
        Helper property to return user email and help IDE resolution.
        """
        return self.user.email


# --- Signals ---

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Automatically creates or updates a Profile instance for each User.
    """
    if created:
        Profile.objects.get_or_create(user=instance)

    # Using getattr to safely handle the profile relationship
    profile = getattr(instance, 'profile', None)
    if profile:
        profile.save()