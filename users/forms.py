from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from phonenumber_field.formfields import PhoneNumberField

User = get_user_model()


class EmailForm(forms.Form):
    """Simple form for sending plain emails."""
    email = forms.EmailField()
    subject = forms.CharField()
    body = forms.CharField(widget=forms.Textarea())


class RegistrationForm(UserCreationForm):
    """
    Form for user registration.
    Note: UserCreationForm already includes password1 and password2 logic.
    """

    class Meta:
        model = User
        # Only include the fields you want to prompt during registration.
        # Password fields are automatically handled by UserCreationForm.
        fields = ("email", "first_name", "last_name")


class ProfileForm(forms.ModelForm):
    """Form to update User and Profile information simultaneously."""

    country = CountryField().formfield(required=False)
    # Changed from 'phone_number' to 'phone_field' to match your model
    phone_field = PhoneNumberField(required=False)
    image = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make email mandatory for profile updates
        if 'email' in self.fields:
            self.fields["email"].required = True

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")