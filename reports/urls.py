from django.urls import path

from reports.views import report_view

app_name = "reports"

urlpatterns = [
    path("", report_view, name="report"),
]
