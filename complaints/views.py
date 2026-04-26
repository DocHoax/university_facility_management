from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from complaints.forms import ComplaintCommentForm, ComplaintForm
from complaints.models import Complaint


@login_required
def complaint_create_view(request):
    if request.method == "POST":
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.department = complaint.department or request.user.department
            complaint.save()
            return redirect("complaints:detail", ticket_id=complaint.ticket_id)
    else:
        form = ComplaintForm()
    return render(request, "complaints/create.html", {"form": form})


@login_required
def complaint_detail_view(request, ticket_id):
    complaint = get_object_or_404(Complaint, ticket_id=ticket_id)
    comment_form = ComplaintCommentForm()
    return render(request, "complaints/detail.html", {"complaint": complaint, "comment_form": comment_form})


@login_required
def complaint_list_view(request):
    complaints = Complaint.objects.select_related("user", "department", "category").order_by("-date_submitted")
    return render(request, "complaints/list.html", {"complaints": complaints})
