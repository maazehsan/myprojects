from django.contrib import admin

from .models import ClientMessage, ProgressScreenshot, ProjectRequest


class ProgressScreenshotInline(admin.TabularInline):
    model = ProgressScreenshot
    extra = 1


class ClientMessageInline(admin.TabularInline):
    model = ClientMessage
    extra = 1
    readonly_fields = ("sender", "message", "created_at")

    def has_add_permission(self, request, obj=None):
        # Admin replies are added via the separate action below
        return True


@admin.register(ProjectRequest)
class ProjectRequestAdmin(admin.ModelAdmin):
    list_display = (
        "project_id", "full_name", "email", "business_name",
        "package", "status", "payment_status", "progress_percentage", "created_at",
    )
    list_filter = ("status", "payment_status", "package", "business_type", "created_at")
    search_fields = ("project_id", "full_name", "email", "business_name")
    readonly_fields = ("project_id", "created_at", "updated_at")
    list_editable = ("status", "payment_status", "progress_percentage")
    ordering = ("-created_at",)
    inlines = [ProgressScreenshotInline, ClientMessageInline]

    fieldsets = (
        ("Project Info", {
            "fields": (
                "project_id", "full_name", "email", "mobile",
                "business_name", "business_type", "description",
                "requirements", "package",
            ),
        }),
        ("Status & Progress", {
            "fields": ("status", "payment_status", "progress_percentage"),
        }),
        ("Invoice", {
            "fields": ("invoice",),
        }),
        ("Admin Remarks", {
            "fields": ("remarks",),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
        }),
    )


@admin.register(ProgressScreenshot)
class ProgressScreenshotAdmin(admin.ModelAdmin):
    list_display = ("project", "caption", "uploaded_at")
    list_filter = ("uploaded_at",)


@admin.register(ClientMessage)
class ClientMessageAdmin(admin.ModelAdmin):
    list_display = ("project", "sender", "message_preview", "created_at")
    list_filter = ("sender", "created_at")
    search_fields = ("project__project_id", "message")

    @admin.display(description="Message")
    def message_preview(self, obj):
        return obj.message[:80] + "..." if len(obj.message) > 80 else obj.message
