from django.conf import settings
from django.db import models
from django.utils import timezone


class ComplaintCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ComplaintStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    ASSIGNED = "ASSIGNED", "Assigned"
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    RESOLVED = "RESOLVED", "Resolved"
    CLOSED = "CLOSED", "Closed"


class Complaint(models.Model):
    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"

    ticket_id = models.CharField(max_length=20, unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="complaints")
    department = models.ForeignKey("accounts.Department", on_delete=models.PROTECT, related_name="complaints")
    category = models.ForeignKey(ComplaintCategory, on_delete=models.PROTECT, related_name="complaints")
    location = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField(max_length=20, choices=ComplaintStatus.choices, default=ComplaintStatus.PENDING)
    attachment = models.FileField(upload_to="complaints/attachments/", blank=True, null=True)
    date_submitted = models.DateTimeField(default=timezone.now)
    date_resolved = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            prefix = timezone.now().strftime("TKT%Y%m%d")
            last = Complaint.objects.filter(ticket_id__startswith=prefix).count() + 1
            self.ticket_id = f"{prefix}{last:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.ticket_id


class ComplaintAssignment(models.Model):
    complaint = models.OneToOneField(Complaint, on_delete=models.CASCADE, related_name="assignment")
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="assigned_complaints")
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="complaints_assigned")
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.complaint.ticket_id} -> {self.assigned_to}"


class ComplaintComment(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="complaint_comments")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.complaint.ticket_id}"
