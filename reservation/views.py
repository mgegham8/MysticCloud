from django.views.generic import CreateView, ListView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from .forms import ReservationForm
from .models import Reservation, Table


class MakeReservationView(LoginRequiredMixin, CreateView):
    """
    Handles the creation of a new table reservation.
    """
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation/reservation.html'
    success_url = reverse_lazy('reservation:view_reservations')

    def form_valid(self, form):
        """
        Processes the form, checking for capacity and availability for the SELECTED date.
        """
        reservation = form.save(commit=False)
        reservation.user = self.request.user
        selected_date = reservation.start_date.date()

        # 1. Capacity Check
        if reservation.number_of_persons > reservation.table.capacity:
            messages.error(
                self.request,
                f"This table's capacity ({reservation.table.capacity}) is less than the number of persons."
            )
            return self.form_invalid(form)

        # 2. Availability Check for the selected date
        already_booked = Reservation.objects.filter(
            table=reservation.table,
            start_date__date=selected_date,
            is_active=True
        ).exists()

        if already_booked:
            messages.error(self.request, f"This table is already reserved for {selected_date}.")
            return self.form_invalid(form)

        # 3. Mark table as unavailable if booking is for today
        if selected_date == timezone.now().date():
            table = reservation.table
            table.is_available = False
            table.save()

        reservation.save()
        messages.success(self.request, "Your table has been reserved successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Passes the current day's booked tables for the visual floor plan.
        """
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        booked_table_ids = Reservation.objects.filter(
            start_date__date=today,
            is_active=True
        ).values_list('table_id', flat=True)

        context['booked_table_ids'] = list(booked_table_ids)
        context['tables'] = Table.objects.all()
        return context

    def form_invalid(self, form):
        messages.error(self.request, "Invalid form submission. Please check the details.")
        return super().form_invalid(form)


class UpdateReservationView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allows a user to update their existing reservation.
    """
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation/reservation.html'
    success_url = reverse_lazy('reservation:view_reservations')

    def test_func(self):
        """Security check: Only the owner can edit."""
        reservation = self.get_object()
        return self.request.user == reservation.user

    def form_valid(self, form):
        reservation = form.save(commit=False)
        selected_date = reservation.start_date.date()

        # 1. Capacity Check
        if reservation.number_of_persons > reservation.table.capacity:
            messages.error(self.request, f"Table capacity ({reservation.table.capacity}) is too small.")
            return self.form_invalid(form)

        # 2. Availability Check (excluding the current reservation being edited)
        already_booked = Reservation.objects.filter(
            table=reservation.table,
            start_date__date=selected_date,
            is_active=True
        ).exclude(pk=self.object.pk).exists()

        if already_booked:
            messages.error(self.request, f"This table is already reserved for {selected_date}.")
            return self.form_invalid(form)

        reservation.save()
        messages.success(self.request, "Your reservation has been updated successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Ensure the map also works in the update view."""
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        booked_table_ids = Reservation.objects.filter(
            start_date__date=today,
            is_active=True
        ).values_list('table_id', flat=True)

        context['booked_table_ids'] = list(booked_table_ids)
        context['tables'] = Table.objects.all()
        return context


class AllReservationsView(LoginRequiredMixin, ListView):
    """
    Displays a list of all active reservations for the logged-in user.
    """
    model = Reservation
    template_name = 'reservation/view_reservations.html'
    context_object_name = 'user_reservations'

    def get_queryset(self):
        return Reservation.objects.filter(
            user=self.request.user,
            is_active=True
        ).order_by('-start_date')


@login_required
def cancel_reservation(request, reservation_id):
    """
    Frees the associated table and marks the reservation as inactive.
    """
    reservation = get_object_or_404(Reservation, pk=reservation_id)

    if request.user == reservation.user:
        table = reservation.table
        table.is_available = True
        table.save()

        reservation.is_active = False
        reservation.save()
        messages.success(request, "Your reservation has been canceled successfully.")
    else:
        messages.error(request, "You do not have permission to cancel this reservation.")

    return redirect("reservation:view_reservations")