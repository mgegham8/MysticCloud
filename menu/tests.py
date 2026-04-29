from django.test import TestCase
from django.urls import reverse
from menu.models import Category, BarCategory, MenuItem, BarItem, Hookah

class MenuModelTest(TestCase):
    """
    Tests for ensuring the models are created correctly and string representations work.
    """
    def setUp(self):
        # Setting up basic data for testing
        self.category = Category.objects.create(name="Food")
        self.bar_category = BarCategory.objects.create(name="Cocktails", category=self.category)
        self.menu_item = MenuItem.objects.create(
            name="Pizza",
            price=15.50,
            category=self.category
        )
        self.hookah = Hookah.objects.create(name="Mint", price=20.00)

    def test_category_creation(self):
        self.assertEqual(str(self.category), "Food")

    def test_menu_item_creation(self):
        self.assertEqual(self.menu_item.name, "Pizza")
        self.assertEqual(float(self.menu_item.price), 15.50)

class MenuViewTest(TestCase):
    """
    Tests for ensuring the views return a 200 OK status and use the correct templates.
    """
    def setUp(self):
        Category.objects.create(name="Dinner")
        BarCategory.objects.create(name="Drinks", category=Category.objects.first())

    def test_menu_list_view(self):
        response = self.client.get(reverse('menu:menu_items'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "menu/menu.html")

    def test_bar_list_view(self):
        response = self.client.get(reverse('menu:bar_items'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "menu/menu.html")

    def test_hookah_list_view(self):
        response = self.client.get(reverse('menu:hookahs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "menu/hookah.html")