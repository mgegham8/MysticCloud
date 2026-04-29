from django.urls import path
from menu.views import (
    MenuListView,
    BarListView,
    HookahListView,
    BarCategoryDetailView,
    BarItemDetailView
)

# Namespace for the menu application
app_name = 'menu'

urlpatterns = [
    # Main listing pages for Food, Bar, and Hookah
    path("", MenuListView.as_view(), name="menu_items"),
    path("bar-items/", BarListView.as_view(), name="bar_items"),
    path("hookahs/", HookahListView.as_view(), name="hookahs"),

    # Individual detail pages for Categories and specific Items
    path('bar-category/<int:pk>/', BarCategoryDetailView.as_view(), name='bar_category_detail'),
    path('bar-item/<int:pk>/', BarItemDetailView.as_view(), name='bar_item_detail'),
]