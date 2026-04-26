from django.urls import path

from complaints.views import (
    complaint_assign_view,
    complaint_create_view,
    complaint_detail_view,
    complaint_list_view,
    category_list_view,
    complaint_track_view,
    complaint_status_update_view,
)

app_name = "complaints"

urlpatterns = [
    path("", complaint_list_view, name="list"),
    path("track/", complaint_track_view, name="track"),
    path("categories/", category_list_view, name="categories"),
    path("create/", complaint_create_view, name="create"),
    path("<str:ticket_id>/assign/", complaint_assign_view, name="assign"),
    path("<str:ticket_id>/status/", complaint_status_update_view, name="status-update"),
    path("<str:ticket_id>/", complaint_detail_view, name="detail"),
]
