from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import Department, User


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "is_active")
    search_fields = ("name", "code")


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("University Details", {"fields": ("phone_number", "department", "role")}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("University Details", {"fields": ("email", "phone_number", "department", "role")}),
    )
    list_display = ("username", "email", "role", "department", "is_staff")
    list_filter = ("role", "is_staff", "is_active", "department")
    search_fields = ("username", "email", "first_name", "last_name")
