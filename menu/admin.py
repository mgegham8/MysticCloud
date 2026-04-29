from django.contrib import admin
from django.utils.html import format_html
from django.templatetags.static import static
from menu.models import MenuItem, BarItem, Category, BarCategory, Hookah


class BaseMenuAdmin(admin.ModelAdmin):
    """
    Base admin class to provide reusable thumbnail preview and common filters.
    """
    list_filter = ("created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at", "thumbnail")

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


class MenuItemAdmin(BaseMenuAdmin):
    list_display = ("name", "category", "price", "thumbnail")
    search_fields = ("name", "description")
    fieldsets = (
        ("GENERAL INFO", {"fields": ("name", "price")}),
        ("DETAILS & CATEGORY", {
            "fields": (
                "category",
                "description",
                ("image", "thumbnail"),
                "created_at",
                "updated_at",
            )
        }),
    )


class BarItemAdmin(BaseMenuAdmin):
    list_display = ("name", "category", "price", "thumbnail")
    search_fields = ("name", "description")
    fieldsets = (
        ("GENERAL INFO", {"fields": ("name", "price")}),
        ("DETAILS & CATEGORY", {
            "fields": (
                "category",
                "description",
                ("image", "thumbnail"),
                "created_at",
                "updated_at",
            )
        }),
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class BarCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    search_fields = ("name",)
    list_filter = ("category",)


class HookahAdmin(admin.ModelAdmin):
    list_display = ("name", "price")
    search_fields = ("name",)


# Registering models to the admin site
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(BarItem, BarItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(BarCategory, BarCategoryAdmin)
admin.site.register(Hookah, HookahAdmin)