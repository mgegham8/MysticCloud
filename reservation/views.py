from django.views.generic import CreateView, ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import ReservationForm
from .models import Reservation, Table


class MakeReservationView(LoginRequiredMixin, CreateView):
    """
    Handles the creation of a new table reservation with availability checks.
    """
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation/reservation.html'
    success_url = reverse_lazy('home:home')

    def form_valid(self, form):
        reservation = form.save(commit=False)
        reservation.user = self.request.user

        # Check for overlapping reservations for the same table
        conflicting_reservations = Reservation.objects.filter(
            table=reservation.table,
            start_date__lt=reservation.end_time,
            end_time__gt=reservation.start_date,
        )

        if conflicting_reservations.exists():
            messages.error(self.request, "Table is not available during the specified time range.")
            return self.form_invalid(form)

        # Check if table capacity can accommodate the group size
        if reservation.number_of_persons > reservation.table.capacity:
            messages.error(self.request,
                           f"This table's capacity ({reservation.table.capacity}) is less than the number of persons.")
            return self.form_invalid(form)

        reservation.save()
        messages.success(self.request, "Your table has been reserved successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Pass all tables to the template for display
        context = super().get_context_data(**kwargs)
        context['tables'] = Table.objects.all()
        return context

    def form_invalid(self, form):
        messages.error(self.request, "Invalid form submission. Please check the details.")
        return super().form_invalid(form)


class AllReservationsView(LoginRequiredMixin, ListView):
    """
    Displays a list of all reservations belonging to the logged-in user.
    """
    model = Reservation
    template_name = 'reservation/view_reservations.html'
    context_object_name = 'user_reservations'

    def get_queryset(self):
        # Ensure users only see their own reservations, sorted by date
        return Reservation.objects.filter(user=self.request.user).order_by('-start_date')


@login_required
def cancel_reservation(request, reservation_id):
    """
    Deletes a reservation if the requesting user owns it.
    """
    # Safely retrieve the reservation or return a 404 error
    reservation = get_object_or_404(Reservation, pk=reservation_id)

    if request.user == reservation.user:
        reservation.delete()
        messages.success(request, "Your reservation has been canceled successfully.")
    else:
        messages.error(request, "You do not have permission to cancel this reservation.")

    return redirect("reservation:view_reservations")