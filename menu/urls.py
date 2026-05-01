from django.urls import path
from .views import MenuListView, BarListView, HookahListView, BarCategoryDetailView

app_name = 'menu'

urlpatterns = [
    path("", MenuListView.as_view(), name="menu_items"),
    path("bar-items/", BarListView.as_view(), name="bar_items"),
    path("hookahs/", HookahListView.as_view(), name="hookahs"),
    path('bar-items/<int:pk>/', BarCategoryDetailView.as_view(), name='bar_item_detail'),
]
