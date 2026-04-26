from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.models import Department
from complaints.models import Complaint, ComplaintAssignment, ComplaintCategory, ComplaintStatus


User = get_user_model()


class ComplaintTests(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="ICT", code="ICT")
        self.category = ComplaintCategory.objects.create(name="Electricity")
        self.admin = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="Password123!",
            department=self.department,
            role=User.Roles.ADMIN,
            is_staff=True,
        )
        self.maintenance = User.objects.create_user(
            username="maint",
            email="maint@example.com",
            password="Password123!",
            department=self.department,
            role=User.Roles.MAINTENANCE,
        )
        self.staff = User.objects.create_user(
            username="staff",
            email="staff@example.com",
            password="Password123!",
            department=self.department,
            role=User.Roles.STAFF,
        )
        self.complaint = Complaint.objects.create(
            user=self.staff,
            department=self.department,
            category=self.category,
            location="Block A",
            description="Power outage in the office",
            priority=Complaint.Priority.HIGH,
        )

    def test_ticket_id_generated(self):
        self.assertTrue(self.complaint.ticket_id.startswith("TKT"))

    def test_public_track_view_returns_complaint(self):
        response = self.client.get(reverse("complaints:track"), {"ticket_id": self.complaint.ticket_id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.complaint.ticket_id)

    def test_admin_can_assign_complaint(self):
        self.client.login(username="admin", password="Password123!")
        response = self.client.post(reverse("complaints:assign", args=[self.complaint.ticket_id]), {"assigned_to": self.maintenance.id})
        self.assertEqual(response.status_code, 302)
        self.complaint.refresh_from_db()
        self.assertEqual(self.complaint.status, ComplaintStatus.ASSIGNED)
        self.assertTrue(ComplaintAssignment.objects.filter(complaint=self.complaint, assigned_to=self.maintenance).exists())

    def test_maintenance_can_update_status(self):
        ComplaintAssignment.objects.create(complaint=self.complaint, assigned_to=self.maintenance, assigned_by=self.admin)
        self.client.login(username="maint", password="Password123!")
        response = self.client.post(reverse("complaints:status-update", args=[self.complaint.ticket_id]), {"status": ComplaintStatus.RESOLVED})
        self.assertEqual(response.status_code, 302)
        self.complaint.refresh_from_db()
        self.assertEqual(self.complaint.status, ComplaintStatus.RESOLVED)
        self.assertIsNotNone(self.complaint.date_resolved)

    def test_admin_can_manage_categories(self):
        self.client.login(username="admin", password="Password123!")
        response = self.client.get(reverse("complaints:categories"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Complaint Categories")

    def test_admin_can_close_complaint(self):
        ComplaintAssignment.objects.create(complaint=self.complaint, assigned_to=self.maintenance, assigned_by=self.admin)
        self.client.login(username="admin", password="Password123!")
        response = self.client.post(reverse("complaints:close", args=[self.complaint.ticket_id]))
        self.assertEqual(response.status_code, 302)
        self.complaint.refresh_from_db()
        self.assertEqual(self.complaint.status, ComplaintStatus.CLOSED)
