from django.urls import path

from notifications.views import notification_live_view, notification_list_view, notification_mark_read_view

app_name = "notifications"

urlpatterns = [
    path("", notification_list_view, name="list"),
    path("live/", notification_live_view, name="live"),
    path("<int:notification_id>/read/", notification_mark_read_view, name="mark-read"),
]
