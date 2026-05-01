from django.views.generic import TemplateView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as Login
from django.contrib.auth import get_user_model, logout
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.views import View
from django.http import HttpResponse
from django.conf import settings
from .forms import RegistrationForm, ProfileForm
from .generate_token import account_activation_token

User = get_user_model()


class RegistrationView(CreateView):
    """Handle user registration and send activation email."""
    form_class = RegistrationForm
    model = User
    success_url = reverse_lazy('home:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        subject = "Authenticate your Profile"
        user = self.object
        user.is_active = False
        user.save()

        token = account_activation_token.make_token(user)
        message = render_to_string("users/authentication.html", {
            "users": user,
            "domain": get_current_site(self.request),
            "token": token,
            "user_pk": user.pk
        })

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email]
        )
        email.send(fail_silently=False)

        messages.success(self.request,
                         "We have sent a link to your email address. Please check it to complete registration.")
        return response


class ValidateUserLink(TemplateView):
    """Validate the activation token from the email link."""

    def get(self, request, *args, **kwargs):
        token = kwargs.get("token")
        pk = kwargs.get("pk")
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return HttpResponse("User not found")

        if account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect("users:login")

        return HttpResponse("Your token is invalid")


class LoginView(Login):
    """Standard login view."""
    pass


class LogoutView(View):
    """Log out the current user."""

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('home:home'))


class UserProfile(LoginRequiredMixin, DetailView):
    """View to display the current authenticated user's profile."""
    model = User
    template_name = "users/user_profile.html"
    context_object_name = "user"

    def get_object(self, queryset=None):
        """Return the currently logged-in user instead of looking for a PK in the URL."""
        return self.request.user


class UserUpdate(LoginRequiredMixin, UpdateView):
    """View to update current user and profile details."""
    model = User
    form_class = ProfileForm
    template_name = "users/update_profile.html"

    def get_object(self, queryset=None):
        """Return the currently logged-in user for updating."""
        return self.request.user

    def get_success_url(self):
        messages.info(self.request, "User updated successfully!")
        return reverse("users:user_profile")

    def form_valid(self, form):
        """Save user data and associated profile extra fields."""
        result = super().form_valid(form)
        # Update additional profile fields from the OneToOne relationship
        profile = self.object.profile
        profile.country = form.cleaned_data.get("country")
        profile.phone_number = form.cleaned_data.get("phone_number")
        profile.image = form.cleaned_data.get("image")
        profile.save()
        return result