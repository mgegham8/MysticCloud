from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView
from django.contrib.auth.views import LoginView as Login
from django.conf import settings
from .forms import RegistrationForm, ProfileForm
from django.contrib.auth import get_user_model, logout
from django.shortcuts import redirect
from django.http import HttpResponse
from .generate_token import account_activation_token

User = get_user_model()


class RegistrationView(CreateView):
    """Handle user registration and send activation email."""
    form_class = RegistrationForm
    model = User
    success_url = '/'

    def form_valid(self, form):
        response = super().form_valid(form)
        subject = "Authenticate your Profile"
        user = self.object
        user.is_active = False
        user.save()
        token = account_activation_token.make_token(user)
        message = render_to_string("users/authentication.html",
                                   {"users": user,
                                    "domain": get_current_site(self.request),
                                    "token": token,
                                    "user_pk": user.pk})
        email = EmailMessage(subject=subject, body=message,
                             from_email=settings.EMAIL_HOST_USER,
                             to=[user.email])
        email.send(fail_silently=False)
        messages.success(self.request, "We have sent a link to your email address,"
                                       " please check it to complete the registration")
        return response


class ValidateUserLink(TemplateView):
    """Validate the activation token from the email link."""
    def get(self, request, *args, **kwargs):
        token = kwargs.get("token")
        pk = kwargs.get("pk")
        user = User.objects.get(pk=pk)
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


class PasswordChangeDoneView(TemplateView):
    """Redirect after successful password change."""
    def get(self, request, **kwargs):
        messages.success(request, "Password changed successfully!")
        return redirect("users:user_profile")


class UserProfile(LoginRequiredMixin, DetailView):
    """View to display the user's own profile using built-in mixin."""
    model = User
    template_name = "users/user_profile.html"


class UserUpdate(LoginRequiredMixin, UpdateView):
    """View to update user and profile details using built-in mixin."""
    model = User
    form_class = ProfileForm

    def get_success_url(self):
        messages.info(self.request, "User updated successfully!")
        return reverse("users:update_profile", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        # Update user data and then save profile fields
        result = super().form_valid(form)
        self.object.profile.country = form.cleaned_data["country"]
        self.object.profile.phone_number = form.cleaned_data["phone_number"]
        self.object.profile.image = form.cleaned_data["image"]
        self.object.profile.save()
        return result