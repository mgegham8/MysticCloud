from django import forms
from django.utils import timezone
from reservation.models import Reservation, Table


class ReservationForm(forms.ModelForm):
    """
    Modern form for table reservations.
    Removed email field and updated widgets for a better user experience.
    """

    class Meta:
        model = Reservation
        # Email field is removed from the list
        fields = ['name', 'phone', 'number_of_persons', 'start_date', 'table']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name',
                'style': 'border-radius: 8px;'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number (e.g. +374...)',
                'style': 'border-radius: 8px;'
            }),
            'number_of_persons': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'style': 'border-radius: 8px;'
            }),
            'start_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'style': 'border-radius: 8px;'
                }
            ),
            # The table field is often handled by the visual map,
            # but we keep it styled here as a fallback.
            'table': forms.Select(attrs={
                'class': 'form-control',
                'style': 'border-radius: 8px;'
            }),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and set up the table queryset.
        """
        super().__init__(*args, **kwargs)
        self.fields['table'].queryset = Table.objects.all()
        self.fields['table'].empty_label = "Select a Table from the map"

    def clean_start_date(self):
        """
        Validation to prevent bookings in the past.
        """
        start_date = self.cleaned_data.get("start_date")
        if start_date and start_date < timezone.now():
            raise forms.ValidationError("You cannot book a table for a past date.")
        return start_date

    def clean(self):
        """
        Cross-field validation for capacity and date-specific availability.
        """
        cleaned_data = super().clean()
        table = cleaned_data.get('table')
        start_date = cleaned_data.get('start_date')
        number_of_persons = cleaned_data.get('number_of_persons')

        if table and start_date:
            # 1. Capacity Check
            if number_of_persons and number_of_persons > table.capacity:
                self.add_error('number_of_persons', f"Maximum capacity for this table is {table.capacity} persons.")

            # 2. Availability Check for the specific date selected
            booking_date = start_date.date()
            is_taken = Reservation.objects.filter(
                table=table,
                start_date__date=booking_date,
                is_active=True
            ).exists()

            if is_taken:
                raise forms.ValidationError("Sorry, this table is already booked for the selected date.")

        return cleaned_data