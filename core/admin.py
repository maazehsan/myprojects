from django.contrib import admin

from .emails import (
    send_project_completed_email,
    send_request_rejected_email,
    send_welcome_email,
)
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

    # ── Email on status change ────────────────────────────────────────────
    _STATUS_EMAIL_MAP = {
        "reviewed": send_welcome_email,
        "completed": send_project_completed_email,
        "rejected": send_request_rejected_email,
    }

    def save_model(self, request, obj, form, change):
        if change and "status" in form.changed_data:
            email_fn = self._STATUS_EMAIL_MAP.get(obj.status)
            if email_fn:
                email_fn(obj)
        super().save_model(request, obj, form, change)

    def save_changelist_formset(self, request, formset, *args, **kwargs):
        """Handle emails when status is changed via list_editable."""
        instances = formset.save(commit=False)
        for instance in instances:
            if instance.pk:
                old = ProjectRequest.objects.filter(pk=instance.pk).values_list("status", flat=True).first()
                if old and old != instance.status:
                    email_fn = self._STATUS_EMAIL_MAP.get(instance.status)
                    if email_fn:
                        email_fn(instance)
        super().save_changelist_formset(request, formset, *args, **kwargs)

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
