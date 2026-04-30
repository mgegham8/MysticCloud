from django.test import TestCase
from django.urls import reverse
from home.models import Chef


class HomeViewsTest(TestCase):

    def test_home_page_status_code(self):
        """Test if the home landing page loads correctly (200 OK)"""
        response = self.client.get(reverse('home:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')

    def test_about_us_page_status_code(self):
        """Test the 'About Us' page status code"""
        # Updated to match name='about_us' in your urls.py
        response = self.client.get(reverse('home:about_us'))
        self.assertEqual(response.status_code, 200)

    def test_chef_list_view(self):
        """Test the chefs list view and data integrity"""
        # Based on your models.py, Chef uses 'name' and 'bio' fields
        Chef.objects.create(
            name="Test Chef",
            bio="Expert in traditional cuisine."
        )

        # Updated to match name='our_chefs' in your urls.py
        response = self.client.get(reverse('home:our_chefs'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Chef")