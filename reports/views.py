from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.db.models import Count
from django.shortcuts import render
from django.utils import timezone
import csv

from complaints.models import Complaint
from reports.forms import ReportFilterForm
from reports.models import Report


def _is_admin(user):
    return user.is_authenticated and user.role == "ADMIN"


@login_required
def report_view(request):
    if not _is_admin(request.user):
        return HttpResponseForbidden("Only administrators can view reports.")

    form = ReportFilterForm(request.GET or None)
    complaints = Complaint.objects.select_related("department", "category", "user")
    filters = {}

    if form.is_valid():
        cleaned = form.cleaned_data
        if cleaned.get("ticket_id"):
            complaints = complaints.filter(ticket_id__icontains=cleaned["ticket_id"])
            filters["ticket_id"] = cleaned["ticket_id"]
        if cleaned.get("status"):
            complaints = complaints.filter(status__iexact=cleaned["status"])
            filters["status"] = cleaned["status"]
        if cleaned.get("category"):
            complaints = complaints.filter(category__name__icontains=cleaned["category"])
            filters["category"] = cleaned["category"]
        if cleaned.get("department"):
            complaints = complaints.filter(department__name__icontains=cleaned["department"])
            filters["department"] = cleaned["department"]
        if cleaned.get("priority"):
            complaints = complaints.filter(priority__iexact=cleaned["priority"])
            filters["priority"] = cleaned["priority"]
        if cleaned.get("start_date"):
            complaints = complaints.filter(date_submitted__date__gte=cleaned["start_date"])
            filters["start_date"] = cleaned["start_date"].isoformat()
        if cleaned.get("end_date"):
            complaints = complaints.filter(date_submitted__date__lte=cleaned["end_date"])
            filters["end_date"] = cleaned["end_date"].isoformat()

    if request.GET.get("export") == "csv":
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="complaints_report.csv"'
        writer = csv.writer(response)
        writer.writerow(["Ticket ID", "User", "Department", "Category", "Priority", "Status", "Date Submitted", "Date Resolved"])
        for complaint in complaints:
            writer.writerow([
                complaint.ticket_id,
                complaint.user.get_full_name() or complaint.user.username,
                complaint.department.name,
                complaint.category.name,
                complaint.priority,
                complaint.status,
                complaint.date_submitted.strftime("%Y-%m-%d %H:%M"),
                complaint.date_resolved.strftime("%Y-%m-%d %H:%M") if complaint.date_resolved else "",
            ])
        Report.objects.create(
            title="Complaints CSV Export",
            report_type=Report.ReportType.SUMMARY,
            generated_by=request.user,
            parameters={"filters": filters, "format": "csv", "generated_at": timezone.now().isoformat()},
        )
        return response

    status_summary = complaints.values("status").annotate(total=Count("id")).order_by("status")
    category_summary = complaints.values("category__name").annotate(total=Count("id")).order_by("-total")
    department_summary = complaints.values("department__name").annotate(total=Count("id")).order_by("-total")
    Report.objects.create(
        title="Complaints Summary Report",
        report_type=Report.ReportType.SUMMARY,
        generated_by=request.user,
        parameters={"filters": filters, "format": "html", "generated_at": timezone.now().isoformat()},
    )
    return render(
        request,
        "reports/admin_report.html",
        {
            "form": form,
            "complaints": complaints.order_by("-date_submitted")[:50],
            "status_summary": status_summary,
            "category_summary": category_summary,
            "department_summary": department_summary,
            "filters": filters,
        },
    )
