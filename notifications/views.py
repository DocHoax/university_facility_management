from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from notifications.models import Notification


@login_required
def notification_list_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "notifications/list.html", {"notifications": notifications})


@login_required
def notification_live_view(request):
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    latest_notification = Notification.objects.filter(user=request.user).order_by("-created_at").first()

    payload = {
        "unread_count": unread_count,
        "has_notifications": latest_notification is not None,
    }

    if latest_notification:
        payload["latest"] = {
            "id": latest_notification.id,
            "title": latest_notification.title,
            "message": latest_notification.message,
            "is_read": latest_notification.is_read,
            "created_at": latest_notification.created_at.isoformat(),
        }

    response = JsonResponse(payload)
    response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response


@login_required
def notification_mark_read_view(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save(update_fields=["is_read"])
    return redirect("notifications:list")
