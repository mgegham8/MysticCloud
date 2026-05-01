from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    LoginView,
    RegistrationView,
    ValidateUserLink,
    LogoutView,
    UserUpdate,
    UserProfile
)

app_name = "users"

urlpatterns = [
    path("login/", LoginView.as_view(template_name='registration/login.html'), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("verify/<int:pk>/<str:token>/", ValidateUserLink.as_view(), name="verify"),
    path("profile/", UserProfile.as_view(), name="user_profile"),
    path("profile/update/", UserUpdate.as_view(), name="update_user"),

    # Password Reset URLs (Add these)
    path("password-reset/", auth_views.PasswordResetView.as_view(), name="reset_password"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
]