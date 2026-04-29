import os
from django.utils.text import slugify

def get_filename(filename):
    """
    Helper function to clean filename and prevent path issues.
    """
    name, ext = os.path.splitext(filename)
    # slugify helps to remove special characters and spaces
    return f"{slugify(name)}{ext}"

def upload_about_us(instance, filename):
    return f"about_us/{slugify(instance.title)}/{get_filename(filename)}"

def upload_why_choose_us(instance, filename):
    return f"why_choose_us/{slugify(instance.title)}/{get_filename(filename)}"

def upload_chef(instance, filename):
    # If the model uses 'name', we slugify it for the path
    return f"chef/{slugify(instance.name)}/{get_filename(filename)}"

def upload_events(instance, filename):
    return f"events/{slugify(instance.name)}/{get_filename(filename)}"

def upload_gallery(instance, filename):
    return f"gallery/{get_filename(filename)}"

def upload_user_images(instance, filename):
    # Ensure instance has a name attribute or use username
    folder_name = slugify(getattr(instance, 'name', 'user'))
    return f"users/{folder_name}/{get_filename(filename)}"

def upload_menu_item_images(instance, filename):
    return f"menu_items/{slugify(instance.name)}/{get_filename(filename)}"

def upload_bar_item_images(instance, filename):
    return f"bar_items/{slugify(instance.name)}/{get_filename(filename)}"