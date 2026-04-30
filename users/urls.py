from django.urls import path
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
    # Login stays the same
    path("login/", LoginView.as_view(template_name='registration/login.html'), name="login"),

    # FIX: Remove template_name and use next_page if needed
    path("logout/", LogoutView.as_view(), name="logout"),

    path("registration/", RegistrationView.as_view(), name="registration"),
    path("verify/<int:pk>/<str:token>/", ValidateUserLink.as_view(), name="verify"),
    path("profile/", UserProfile.as_view(), name="user_profile"),
    path("profile/update/", UserUpdate.as_view(), name="update_user"),
]