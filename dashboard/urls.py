from django.urls import path

from dashboard.views import admin_dashboard, home, manage_departments_view, manage_users_view, maintenance_dashboard, staff_dashboard

app_name = "dashboard"

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin_dashboard, name="admin"),
    path("admin/users/", manage_users_view, name="manage-users"),
    path("admin/users/<int:user_id>/", manage_users_view, name="edit-user"),
    path("admin/departments/", manage_departments_view, name="manage-departments"),
    path("admin/departments/<int:department_id>/", manage_departments_view, name="edit-department"),
    path("maintenance/", maintenance_dashboard, name="maintenance"),
    path("staff/", staff_dashboard, name="staff"),
]
