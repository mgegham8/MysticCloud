from django.urls import path
from .views import (
    HomeView,
    AboutUsView,
    ContactUsView,
    ChefUsView,
    GalleryView,
    EventsView
)

# Namespace for the 'home' app
app_name = "home"

urlpatterns = [
    # Main landing page
    path("", HomeView.as_view(), name="home"),

    # Static info pages
    path('about-us/', AboutUsView.as_view(), name='about_us'),
    path('contact-us/', ContactUsView.as_view(), name='contact_us'),

    # List-based pages (Chefs, Gallery, Events)
    path('our-chefs/', ChefUsView.as_view(), name='our_chefs'),
    path('galleries/', GalleryView.as_view(), name='galleries'),
    path('our-events/', EventsView.as_view(), name='our_events'),
]