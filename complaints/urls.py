from django.urls import path

from complaints.views import complaint_create_view, complaint_detail_view, complaint_list_view

app_name = "complaints"

urlpatterns = [
    path("", complaint_list_view, name="list"),
    path("create/", complaint_create_view, name="create"),
    path("<str:ticket_id>/", complaint_detail_view, name="detail"),
]
