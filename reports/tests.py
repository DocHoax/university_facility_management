from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.models import Department
from complaints.models import Complaint, ComplaintCategory
from reports.models import Report


User = get_user_model()


class ReportTests(TestCase):
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
            location="Office 2",
            description="Network drop in office",
            priority=Complaint.Priority.MEDIUM,
        )

    def test_report_view_requires_admin(self):
        response = self.client.get(reverse("reports:report"))
        self.assertEqual(response.status_code, 302)

    def test_report_view_creates_report_record(self):
        self.client.login(username="admin", password="Password123!")
        response = self.client.get(reverse("reports:report"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Admin Report")
        self.assertTrue(Report.objects.filter(title="Complaints Summary Report").exists())

    def test_csv_export_creates_report_record(self):
        self.client.login(username="admin", password="Password123!")
        response = self.client.get(reverse("reports:report"), {"export": "csv"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertTrue(Report.objects.filter(title="Complaints CSV Export").exists())
