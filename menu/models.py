from django.db import models
from django.urls import reverse
from helpers.media_upload import upload_menu_item_images, upload_bar_item_images

class Category(models.Model):
    """
    General categories for the food menu (e.g., Appetizers, Main Course).
    """
    name = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class BarCategory(models.Model):
    """
    Categories specifically for bar items (e.g., Cocktails, Spirits, Soft Drinks).
    """
    name = models.CharField(max_length=250)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='bar_category_items'
    )

    class Meta:
        verbose_name_plural = "Bar Categories"

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """
    Individual food items within a specific food category.
    """
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=upload_menu_item_images, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='menu_items'
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        Returns the URL for the main menu view.
        """
        return reverse('menu:menu_items')


class BarItem(models.Model):
    """
    Individual drinks or products within a bar category.
    """
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=upload_bar_item_images, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        BarCategory,
        on_delete=models.CASCADE,
        related_name='bar_items'
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        Returns the URL to access a specific bar item detail page.
        """
        return reverse('menu:bar_item_detail', args=[str(self.id)])


class Hookah(models.Model):
    """
    Available hookah flavors and their pricing.
    """
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name