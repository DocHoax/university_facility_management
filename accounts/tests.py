from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.models import Department


User = get_user_model()


class AccountsTests(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="ICT", code="ICT")
        self.user = User.objects.create_user(
            username="john",
            email="john@example.com",
            password="Password123!",
            department=self.department,
            role=User.Roles.STAFF,
        )

    def test_profile_requires_login(self):
        response = self.client.get(reverse("accounts:profile"))
        self.assertEqual(response.status_code, 302)

    def test_login_with_email(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "john@example.com", "password": "Password123!"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["user"].is_authenticated)

    def test_register_logs_user_in(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "jane",
                "email": "jane@example.com",
                "phone_number": "08012345678",
                "department": self.department.id,
                "role": User.Roles.STAFF,
                "first_name": "Jane",
                "last_name": "Doe",
                "password1": "Password123!",
                "password2": "Password123!",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["user"].is_authenticated)
