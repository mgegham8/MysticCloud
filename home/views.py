from django.views import View
from django.views.generic import ListView, TemplateView
from django.shortcuts import render
from home.models import AboutUs, WhyChooseUs, Chef, ContactUs, Gallery, Events
from menu.models import Category, MenuItem, BarCategory, Hookah

class HomeView(TemplateView):
    """
    Main landing page view that aggregates data from multiple models.
    """
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Using select_related and prefetch_related for database optimization
        context['categories'] = Category.objects.all()
        context['menu_items'] = MenuItem.objects.select_related("category").all()
        context['bar_categories'] = BarCategory.objects.all()
        context['hookahs'] = Hookah.objects.all()
        context['events'] = Events.objects.all()
        context['our_chefs'] = Chef.objects.all()
        context['gallery_images'] = Gallery.objects.all()
        return context


class AboutUsView(TemplateView):
    """
    Displays information about the restaurant.
    """
    template_name = 'home/about.html'


class ContactUsView(TemplateView):
    """
    Displays contact information and location.
    """
    template_name = 'home/contact_us.html'


class ChefUsView(ListView):
    """
    Displays a list of all chefs. Refactored from View to ListView for consistency.
    """
    model = Chef
    template_name = "home/chefs.html"
    context_object_name = 'our_chefs'


class GalleryView(ListView):
    """
    Displays a gallery of images using Django's built-in ListView.
    """
    model = Gallery
    template_name = 'home/gallery.html'
    context_object_name = 'gallery_images'


class EventsView(ListView):
    """
    Displays all upcoming events. Refactored to ListView.
    """
    model = Events
    template_name = "home/events.html"
    context_object_name = 'events'