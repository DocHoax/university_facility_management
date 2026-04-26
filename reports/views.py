from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render

from complaints.models import Complaint


@login_required
def report_view(request):
    status_summary = Complaint.objects.values("status").annotate(total=Count("id")).order_by("status")
    category_summary = Complaint.objects.values("category__name").annotate(total=Count("id")).order_by("-total")
    return render(
        request,
        "reports/admin_report.html",
        {"status_summary": status_summary, "category_summary": category_summary},
    )
