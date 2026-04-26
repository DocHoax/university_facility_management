from django.urls import path

from notifications.views import notification_list_view, notification_mark_read_view

app_name = "notifications"

urlpatterns = [
    path("", notification_list_view, name="list"),
    path("<int:notification_id>/read/", notification_mark_read_view, name="mark-read"),
]
