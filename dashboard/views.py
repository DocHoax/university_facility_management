from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import redirect, render

from complaints.models import Complaint, ComplaintStatus


@login_required
def home(request):
    role = request.user.role
    if role == "ADMIN":
        return redirect("dashboard:admin")
    if role == "MAINTENANCE":
        return redirect("dashboard:maintenance")
    return redirect("dashboard:staff")


@login_required
def admin_dashboard(request):
    counts = Complaint.objects.values("status").annotate(total=Count("id"))
    summary = {item["status"]: item["total"] for item in counts}
    context = {
        "total_complaints": Complaint.objects.count(),
        "pending_complaints": summary.get(ComplaintStatus.PENDING, 0),
        "in_progress_complaints": summary.get(ComplaintStatus.IN_PROGRESS, 0),
        "resolved_complaints": summary.get(ComplaintStatus.RESOLVED, 0),
        "complaints": Complaint.objects.select_related("user", "department", "category")[:20],
    }
    return render(request, "dashboard/admin.html", context)


@login_required
def maintenance_dashboard(request):
    complaints = Complaint.objects.filter(status__in=[ComplaintStatus.ASSIGNED, ComplaintStatus.IN_PROGRESS]).select_related(
        "user", "department", "category"
    )
    return render(request, "dashboard/maintenance.html", {"complaints": complaints})


@login_required
def staff_dashboard(request):
    complaints = Complaint.objects.filter(user=request.user).select_related("department", "category")
    return render(request, "dashboard/staff.html", {"complaints": complaints})
