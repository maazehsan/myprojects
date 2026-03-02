from django.contrib import admin

from .models import ProjectRequest


@admin.register(ProjectRequest)
class ProjectRequestAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "business_name", "package", "status", "created_at")
    list_filter = ("status", "package", "business_type", "created_at")
    search_fields = ("full_name", "email", "business_name")
    readonly_fields = ("created_at", "updated_at")
    list_editable = ("status",)
    ordering = ("-created_at",)
