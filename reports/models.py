from django.conf import settings
from django.db import models


class Report(models.Model):
    class ReportType(models.TextChoices):
        SUMMARY = "SUMMARY", "Summary"
        STATUS = "STATUS", "Status"
        CATEGORY = "CATEGORY", "Category"
        DEPARTMENT = "DEPARTMENT", "Department"

    title = models.CharField(max_length=255)
    report_type = models.CharField(max_length=20, choices=ReportType.choices, default=ReportType.SUMMARY)
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="generated_reports")
    parameters = models.JSONField(default=dict, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
