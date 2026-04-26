from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.models import Department
from notifications.models import Notification


User = get_user_model()


class NotificationTests(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="ICT", code="ICT")
        self.user = User.objects.create_user(
            username="john",
            email="john@example.com",
            password="Password123!",
            department=self.department,
            role=User.Roles.STAFF,
        )
        self.notification = Notification.objects.create(user=self.user, title="Complaint submitted", message="Received")

    def test_mark_read(self):
        self.client.login(username="john", password="Password123!")
        response = self.client.get(reverse("notifications:mark-read", args=[self.notification.id]))
        self.assertEqual(response.status_code, 302)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)
