from django.urls import path
from .views import MakeReservationView, cancel_reservation, AllReservationsView

# Namespace for the reservation application
app_name = "reservation"

urlpatterns = [
    # Booking and management pages
    path('reservation/', MakeReservationView.as_view(), name='reservation'),
    path('view-reservations/', AllReservationsView.as_view(), name='view_reservations'),

    # Action paths
    path('cancel-reservation/<int:reservation_id>/', cancel_reservation, name='cancel_reservation'),
]