import os
import uuid
from django.utils.text import slugify

def get_filename(filename):
    """
    Cleans the filename and appends a unique short ID to prevent duplicates.
    Example: 'My Image #1.jpg' -> 'my-image-1-a2b3c4.jpg'
    """
    name, ext = os.path.splitext(filename)
    # Generate a short unique ID to avoid overwriting files with the same name
    unique_id = uuid.uuid4().hex[:6]
    return f"{slugify(name)}-{unique_id}{ext}"

def upload_about_us(instance, filename):
    """Path: media/about_us/title-slug/filename.ext"""
    return f"about_us/{slugify(instance.title)}/{get_filename(filename)}"

def upload_why_choose_us(instance, filename):
    """Path: media/why_choose_us/title-slug/filename.ext"""
    return f"why_choose_us/{slugify(instance.title)}/{get_filename(filename)}"

def upload_chef(instance, filename):
    """Path: media/chef/name-slug/filename.ext"""
    return f"chef/{slugify(instance.name)}/{get_filename(filename)}"

def upload_events(instance, filename):
    """Path: media/events/name-slug/filename.ext"""
    return f"events/{slugify(instance.name)}/{get_filename(filename)}"

def upload_gallery(instance, filename):
    """Path: media/gallery/filename.ext"""
    return f"gallery/{get_filename(filename)}"

def upload_user_images(instance, filename):
    """
    Path: media/users/user-name/filename.ext
    Uses a safe fallback if the name attribute is missing.
    """
    folder_name = slugify(getattr(instance, 'name', 'user'))
    return f"users/{folder_name}/{get_filename(filename)}"

def upload_menu_item_images(instance, filename):
    """Path: media/menu_items/item-name/filename.ext"""
    return f"menu_items/{slugify(instance.name)}/{get_filename(filename)}"

def upload_bar_item_images(instance, filename):
    """Path: media/bar_items/item-name/filename.ext"""
    return f"bar_items/{slugify(instance.name)}/{get_filename(filename)}"