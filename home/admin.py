from django.contrib import admin
from django.utils.html import format_html
from django.templatetags.static import static
from home.models import AboutUs, Chef, WhyChooseUs, ContactUs, FollowUs, Gallery, Events

# Global Admin Interface Customization
admin.site.site_header = "Mystic Cloud Administration"
admin.site.site_title = "Mystic Cloud Admin Portal"
admin.site.index_title = "Welcome to the Control Panel"


class BaseImageAdmin(admin.ModelAdmin):
    """
    Base class to provide a reusable thumbnail preview for models with images.
    """
    readonly_fields = ("thumbnail",)

    @admin.display(description="Preview")
    def thumbnail(self, obj):
        if hasattr(obj, 'image') and obj.image:
            url = obj.image.url
        else:
            url = static("img/no_image.jpg")

        return format_html(
            "<img src='{}' style='width: 50px; height: 50px; object-fit: cover; border-radius: 5px;'>",
            url
        )


class AboutUsAdmin(BaseImageAdmin):
    list_display = ("title", "content", "thumbnail")
    list_display_links = ("title",)
    search_fields = ("title",)
    fieldsets = (
        ("GENERAL INFORMATION", {"fields": ("title",)}),
        ("CONTENT & MEDIA", {"fields": ("content", ("image", "thumbnail"))}),
    )


class WhyChooseUsAdmin(BaseImageAdmin):
    list_display = ("title", "content", "thumbnail")
    list_display_links = ("title",)
    search_fields = ("title",)
    fieldsets = (
        ("PROMOTION DETAILS", {"fields": ("title",)}),
        ("CONTENT & MEDIA", {"fields": ("content", ("image", "thumbnail"))}),
    )


class ChefAdmin(BaseImageAdmin):
    list_display = ("name", "bio", "thumbnail")
    list_display_links = ("name",)
    search_fields = ("name",)
    fieldsets = (
        ("PERSONAL INFO", {"fields": ("name",)}),
        ("BIOGRAPHY & PHOTO", {"fields": ("bio", ("image", "thumbnail"))}),
    )


@admin.register(FollowUs)
class FollowUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('address', 'phone_number', 'email', 'opening_hours')


# Registering models to the admin site
admin.site.register(AboutUs, AboutUsAdmin)
admin.site.register(WhyChooseUs, WhyChooseUsAdmin)
admin.site.register(Chef, ChefAdmin)
admin.site.register(Gallery)
admin.site.register(Events)