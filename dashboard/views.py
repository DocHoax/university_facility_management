from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Department, User
from dashboard.forms import AdminUserForm, DepartmentForm
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


def _require_admin(user):
    return user.is_authenticated and user.role == "ADMIN"


@login_required
def manage_users_view(request, user_id=None):
    if not _require_admin(request.user):
        return HttpResponseForbidden("Only administrators can manage users.")

    selected_user = get_object_or_404(User, pk=user_id) if user_id else None
    if request.method == "POST":
        form = AdminUserForm(request.POST, instance=selected_user)
        if form.is_valid():
            form.save()
            return redirect("dashboard:manage-users")
    else:
        form = AdminUserForm(instance=selected_user)

    users = User.objects.select_related("department").order_by("first_name", "username")
    return render(request, "dashboard/users.html", {"form": form, "users": users, "selected_user": selected_user})


@login_required
def manage_departments_view(request, department_id=None):
    if not _require_admin(request.user):
        return HttpResponseForbidden("Only administrators can manage departments.")

    selected_department = get_object_or_404(Department, pk=department_id) if department_id else None
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=selected_department)
        if form.is_valid():
            form.save()
            return redirect("dashboard:manage-departments")
    else:
        form = DepartmentForm(instance=selected_department)

    departments = Department.objects.order_by("name")
    return render(
        request,
        "dashboard/departments.html",
        {"form": form, "departments": departments, "selected_department": selected_department},
    )
