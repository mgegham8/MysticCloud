from django.views.generic import DetailView, ListView
from menu.models import Category, BarItem, BarCategory, Hookah

class MenuListView(ListView):
    """
    Displays the full food menu grouped by categories.
    """
    model = Category
    template_name = "menu/menu.html"
    context_object_name = 'categories'

    def get_queryset(self):
        # Prefetching related items to minimize database hits
        return Category.objects.prefetch_related("menu_items", "bar_category_items").all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adding bar categories to the food menu context if needed
        context['bar_categories'] = BarCategory.objects.all()
        return context


class BarListView(ListView):
    """
    Displays the bar menu with categories and their specific items.
    """
    model = BarCategory
    template_name = "menu/menu.html"
    context_object_name = 'bar_categories'

    def get_queryset(self):
        # Optimization for loading all bar items at once
        return BarCategory.objects.prefetch_related("bar_items").all()


class HookahListView(ListView):
    """
    Displays the list of available hookah flavors and prices.
    """
    model = Hookah
    template_name = "menu/hookah.html"
    context_object_name = "hookahs"


class BarCategoryDetailView(DetailView):
    """
    Detailed view for a specific bar category and its contents.
    """
    model = BarCategory
    template_name = "menu/bar_item_detail.html"
    context_object_name = "bar_item_detail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Explicitly fetching bar items for the selected category
        context['bar_items'] = self.object.bar_items.all()
        return context


class BarItemDetailView(DetailView):
    """
    Detailed view for a single bar item or drink.
    """
    model = BarItem
    template_name = "menu/bar_item_detail.html"
    context_object_name = "bar_item_detail"