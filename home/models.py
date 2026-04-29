from django.db import models
from helpers.media_upload import (
    upload_about_us,
    upload_chef,
    upload_why_choose_us,
    upload_gallery,
    upload_events
)

class AboutUs(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to=upload_about_us)

    class Meta:
        verbose_name = "About Us"
        verbose_name_plural = "About Us"

    def __str__(self):
        return self.title


class WhyChooseUs(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to=upload_why_choose_us)

    class Meta:
        verbose_name = "Why Choose Us"
        verbose_name_plural = "Why Choose Us"

    def __str__(self):
        return self.title


class Chef(models.Model):
    name = models.CharField(max_length=50)
    bio = models.TextField()
    image = models.ImageField(upload_to=upload_chef)

    def __str__(self):
        return self.name


class Gallery(models.Model):
    image = models.ImageField(upload_to=upload_gallery)
    created_at = models.DateTimeField(auto_now_add=True) # Useful for sorting

    class Meta:
        verbose_name_plural = "Galleries"

    def __str__(self):
        return f"Gallery Image {self.id}"


class FollowUs(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField()

    class Meta:
        verbose_name = "Social Link"
        verbose_name_plural = "Social Links"

    def __str__(self):
        return self.name


class ContactUs(models.Model):
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    opening_hours = models.CharField(max_length=100)
    follow_us = models.ManyToManyField(
        FollowUs,
        blank=True,
        related_name="contacts"
    )

    class Meta:
        verbose_name = "Contact Info"
        verbose_name_plural = "Contact Info"

    def __str__(self):
        return f"Contact: {self.email}"


class Events(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to=upload_events)
    date = models.DateTimeField(null=True, blank=True) # Events usually have a date

    class Meta:
        verbose_name_plural = "Events"

    def __str__(self):
        return self.name