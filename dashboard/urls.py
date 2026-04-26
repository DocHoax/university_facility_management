from django.urls import path

from dashboard.views import admin_dashboard, home, maintenance_dashboard, staff_dashboard

app_name = "dashboard"

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin_dashboard, name="admin"),
    path("maintenance/", maintenance_dashboard, name="maintenance"),
    path("staff/", staff_dashboard, name="staff"),
]
