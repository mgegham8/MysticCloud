from django.views.generic import DetailView, ListView
from .models import Category, BarItem, BarCategory, Hookah

class MenuListView(ListView):
    model = Category
    template_name = "menu/menu.html"
    context_object_name = 'categories'

    def get_queryset(self):
        # Օպտիմիզացված բեռնում
        return Category.objects.prefetch_related("menu_items").all()

class BarListView(ListView):
    model = BarCategory
    template_name = "menu/bar_list.html"  # Սա քո նոր սիրուն template-ն է
    context_object_name = 'bar_categories'

    def get_queryset(self):
        # Քանի որ քո հին կոդում կար "bar_items", օգտագործում ենք դա
        return BarCategory.objects.prefetch_related("bar_items").all()

class HookahListView(ListView): # Դարձրեցի ListView ավելի մաքուր կոդի համար
    model = Hookah
    template_name = "menu/hookah.html"
    context_object_name = "hookahs"

class BarCategoryDetailView(DetailView):
    model = BarCategory
    template_name = "menu/bar_item_detail.html"
    context_object_name = "bar_item_detail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Օգտագործում ենք նույն "bar_items" կապը
        context['bar_items'] = self.object.bar_items.all()
        return context

class BarItemDetailView(DetailView):
    model = BarItem
    template_name = "menu/bar_item_detail.html"
    context_object_name = "bar_item_detail"