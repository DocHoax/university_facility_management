from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.models import User
from complaints.forms import ComplaintAssignmentForm, ComplaintCommentForm, ComplaintForm, ComplaintStatusUpdateForm, ComplaintTrackForm
from complaints.models import Complaint, ComplaintAssignment, ComplaintComment, ComplaintStatus
from notifications.services import create_notification


def _is_admin(user):
    return user.is_authenticated and user.role == "ADMIN"


def _is_maintenance(user):
    return user.is_authenticated and user.role == "MAINTENANCE"


def _notify(user, title, message):
    create_notification(user, title, message)


def _email(user, subject, body):
    if user.email:
        send_mail(subject, body, None, [user.email], fail_silently=True)


@login_required
def complaint_create_view(request):
    if request.method == "POST":
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.department = complaint.department or request.user.department
            complaint.save()
            _notify(request.user, f"Complaint {complaint.ticket_id} submitted", "Your complaint has been received and is pending review.")
            return redirect("complaints:detail", ticket_id=complaint.ticket_id)
    else:
        form = ComplaintForm()
    return render(request, "complaints/create.html", {"form": form})


@login_required
def complaint_detail_view(request, ticket_id):
    complaint = get_object_or_404(Complaint, ticket_id=ticket_id)
    if request.method == "POST":
        comment_form = ComplaintCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.complaint = complaint
            comment.author = request.user
            comment.save()
            return redirect("complaints:detail", ticket_id=ticket_id)
    else:
        comment_form = ComplaintCommentForm()
    return render(request, "complaints/detail.html", {"complaint": complaint, "comment_form": comment_form})


@login_required
def complaint_list_view(request):
    complaints = Complaint.objects.select_related("user", "department", "category")
    ticket_id = request.GET.get("ticket_id", "").strip()
    status = request.GET.get("status", "").strip()
    category = request.GET.get("category", "").strip()
    priority = request.GET.get("priority", "").strip()

    if ticket_id:
        complaints = complaints.filter(ticket_id__icontains=ticket_id)
    if status:
        complaints = complaints.filter(status=status)
    if category:
        complaints = complaints.filter(category_id=category)
    if priority:
        complaints = complaints.filter(priority=priority)

    complaints = complaints.order_by("-date_submitted")
    return render(
        request,
        "complaints/list.html",
        {"complaints": complaints, "ticket_id": ticket_id, "status": status, "category": category, "priority": priority},
    )


def complaint_track_view(request):
    complaint = None
    form = ComplaintTrackForm(request.GET or None)
    if form.is_valid():
        ticket_id = form.cleaned_data["ticket_id"]
        complaint = Complaint.objects.select_related("user", "department", "category").prefetch_related("comments").filter(ticket_id__iexact=ticket_id).first()
    return render(request, "complaints/track.html", {"form": form, "complaint": complaint})


@login_required
def complaint_assign_view(request, ticket_id):
    if not _is_admin(request.user):
        return HttpResponseForbidden("Only administrators can assign complaints.")

    complaint = get_object_or_404(Complaint, ticket_id=ticket_id)
    maintenance_users = User.objects.filter(role="MAINTENANCE")
    if request.method == "POST":
        form = ComplaintAssignmentForm(request.POST, user_queryset=maintenance_users)
        if form.is_valid():
            assigned_to = form.cleaned_data["assigned_to"]
            ComplaintAssignment.objects.update_or_create(
                complaint=complaint,
                defaults={"assigned_to": assigned_to, "assigned_by": request.user},
            )
            complaint.status = ComplaintStatus.ASSIGNED
            complaint.save(update_fields=["status"])
            _notify(assigned_to, f"Complaint {complaint.ticket_id} assigned", "A new complaint has been assigned to you.")
            _notify(complaint.user, f"Complaint {complaint.ticket_id} assigned", "Your complaint has been assigned to maintenance staff.")
            _email(assigned_to, f"Complaint {complaint.ticket_id} assigned", complaint.description)
            messages.success(request, "Complaint assigned successfully.")
            return redirect("complaints:detail", ticket_id=ticket_id)
    else:
        form = ComplaintAssignmentForm(user_queryset=maintenance_users)
    return render(request, "complaints/assign.html", {"complaint": complaint, "form": form})


@login_required
def complaint_status_update_view(request, ticket_id):
    if not _is_maintenance(request.user):
        return HttpResponseForbidden("Only maintenance staff can update complaint status.")

    complaint = get_object_or_404(Complaint, ticket_id=ticket_id)
    if request.method == "POST":
        form = ComplaintStatusUpdateForm(request.POST)
        if form.is_valid():
            complaint.status = form.cleaned_data["status"]
            if complaint.status == ComplaintStatus.RESOLVED:
                complaint.date_resolved = complaint.date_resolved or timezone.now()
            complaint.save(update_fields=["status", "date_resolved"])
            _notify(complaint.user, f"Complaint {complaint.ticket_id} updated", f"Your complaint status is now {complaint.status}.")
            _email(complaint.user, f"Complaint {complaint.ticket_id} status update", f"Status updated to {complaint.status}.")
            messages.success(request, "Complaint status updated.")
            return redirect("complaints:detail", ticket_id=ticket_id)
    else:
        form = ComplaintStatusUpdateForm(initial={"status": complaint.status})
    return render(request, "complaints/status_update.html", {"complaint": complaint, "form": form})
