from django.contrib import admin

from complaints.models import Complaint, ComplaintAssignment, ComplaintCategory, ComplaintComment


@admin.register(ComplaintCategory)
class ComplaintCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name",)


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ("ticket_id", "user", "department", "category", "priority", "status", "date_submitted")
    list_filter = ("status", "priority", "department", "category")
    search_fields = ("ticket_id", "user__username", "user__email")


@admin.register(ComplaintAssignment)
class ComplaintAssignmentAdmin(admin.ModelAdmin):
    list_display = ("complaint", "assigned_to", "assigned_by", "assigned_at")


@admin.register(ComplaintComment)
class ComplaintCommentAdmin(admin.ModelAdmin):
    list_display = ("complaint", "author", "created_at")
