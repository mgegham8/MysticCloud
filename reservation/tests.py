from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from reservation.models import Table, Reservation

User = get_user_model()


class ReservationLogicTest(TestCase):
    """
    Tests for reservation creation and access control.
    """

    def setUp(self):
        # Ստեղծում ենք օգտատեր միայն email-ով և password-ով
        self.user_email = "test@example.com"
        self.password = "password123"
        self.user = User.objects.create_user(
            email=self.user_email,
            password=self.password
        )

        self.table = Table.objects.create(table_number=1, capacity=4)

        # Ժամանակային միջակայք թեստերի համար
        self.start_time = timezone.now() + timedelta(days=1)
        self.end_time = self.start_time + timedelta(hours=2)

    def test_reservation_creation(self):
        """Test if a simple reservation is created successfully."""
        reservation = Reservation.objects.create(
            name="John Doe",
            phone="123456789",
            number_of_persons=2,
            user=self.user,
            table=self.table,
            start_date=self.start_time,
            end_time=self.end_time
        )
        self.assertEqual(reservation.name, "John Doe")
        # Ստուգիր քո models.py-ի related_name-ը (կա՛մ reservations, կա՛մ reserved_table)
        self.assertEqual(self.table.reservations.count(), 1)

    def test_view_access_logged_in(self):
        """Check if logged-in user can access the reservation page."""
        # Լոգին ենք լինում email-ով
        self.client.login(email=self.user_email, password=self.password)
        response = self.client.get(reverse('reservation:reservation'))
        self.assertEqual(response.status_code, 200)

    def test_view_access_anonymous(self):
        """Anonymous users should be redirected to login (302)."""
        response = self.client.get(reverse('reservation:reservation'))
        self.assertEqual(response.status_code, 302)