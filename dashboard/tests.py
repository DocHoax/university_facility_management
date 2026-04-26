from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.models import Department
from complaints.models import Complaint, ComplaintCategory


User = get_user_model()


class DashboardTests(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="ICT", code="ICT")
        self.category = ComplaintCategory.objects.create(name="Internet")
        self.admin = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="Password123!",
            department=self.department,
            role=User.Roles.ADMIN,
            is_staff=True,
        )
        self.staff = User.objects.create_user(
            username="staff",
            email="staff@example.com",
            password="Password123!",
            department=self.department,
            role=User.Roles.STAFF,
        )
        Complaint.objects.create(
            user=self.staff,
            department=self.department,
            category=self.category,
            location="Office 1",
            description="No internet connection",
            priority=Complaint.Priority.MEDIUM,
        )

    def test_admin_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard:admin"))
        self.assertEqual(response.status_code, 302)

    def test_manage_users_page_loads_for_admin(self):
        self.client.login(username="admin", password="Password123!")
        response = self.client.get(reverse("dashboard:manage-users"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Manage Users")

    def test_manage_departments_page_loads_for_admin(self):
        self.client.login(username="admin", password="Password123!")
        response = self.client.get(reverse("dashboard:manage-departments"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Manage Departments")

    def test_report_page_loads_for_admin(self):
        self.client.login(username="admin", password="Password123!")
        response = self.client.get(reverse("reports:report"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Admin Report")
