from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
from .models import Profile

User = get_user_model()


class UserAccountTests(TestCase):
    """
    Test suite for user registration, authentication, and profile logic.
    """

    def setUp(self):
        """Set up initial data for tests."""
        self.register_url = reverse('users:registration')
        self.login_url = reverse('users:login')
        self.user_data = {
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }

    def test_registration_creates_user_and_profile(self):
        """
        Test that registration creates a user, sends an email,
        and triggers profile creation via signals.
        """
        response = self.client.post(self.register_url, self.user_data)

        # Check if user was created and is inactive
        user = User.objects.get(email='testuser@example.com')
        self.assertFalse(user.is_active)

        # Check if signal automatically created a profile
        self.assertTrue(Profile.objects.filter(user=user).exists())

        # Check if activation email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Authenticate your Profile", mail.outbox[0].subject)

    def test_login_functionality(self):
        """Test if an active user can log in successfully."""
        # Create an active user
        user = User.objects.create_user(
            email='active@example.com',
            password='password123',
            is_active=True
        )

        response = self.client.post(self.login_url, {
            'username': 'active@example.com',
            'password': 'password123'
        })

        # Check if redirected after login (usually to success_url or root)
        self.assertEqual(response.status_code, 302)

    def test_profile_access_requires_login(self):
        """Ensure that unauthenticated users cannot access the profile page."""
        profile_url = reverse('users:user_profile')
        response = self.client.get(profile_url)

        # Should redirect to login page
        self.assertRedirects(response, f"{reverse('users:login')}?next={profile_url}")

    def test_user_can_only_view_own_profile(self):
        """
        Test security: user should only see their own data
        regardless of URL parameters (based on our view logic).
        """
        user = User.objects.create_user(
            email='owner@example.com',
            password='password123',
            is_active=True
        )
        self.client.login(email='owner@example.com', password='password123')

        response = self.client.get(reverse('users:user_profile'))
        self.assertEqual(response.status_code, 200)
        # Check if the context contains the correct user object
        self.assertEqual(response.context['user_obj'], user)