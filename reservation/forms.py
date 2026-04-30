from django import forms
from reservation.models import Reservation, Table


class ReservationForm(forms.ModelForm):
    """
    Form for creating and managing table reservations.
    Includes custom widgets for date and time selection.
    """

    class Meta:
        model = Reservation
        fields = ['name', 'email', 'phone', 'number_of_persons', 'start_date', 'end_time', 'table']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'number_of_persons': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'start_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'end_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'table': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Custom initialization to set up table querysets or other dynamic data.
        """
        super().__init__(*args, **kwargs)
        # You can filter tables here if needed (e.g., only active tables)
        self.fields['table'].queryset = Table.objects.all()
        # Optionally, you can customize the label for the table dropdown
        self.fields['table'].empty_label = "Select a Table"

    def clean(self):
        """
        Custom validation to ensure end_time is after start_date.
        """
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_time = cleaned_data.get("end_time")

        if start_date and end_time and end_time <= start_date:
            raise forms.ValidationError("End time must be after the start date.")

        return cleaned_data