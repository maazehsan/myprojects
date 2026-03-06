import random
import string

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


def generate_project_id():
    """Generate a unique 5-digit random number ID."""
    return "".join(random.choices(string.digits, k=5))


class ProjectRequest(models.Model):
    """Stores project requests submitted from the frontend form."""

    BUSINESS_TYPE_CHOICES = [
        ("Startup", "Startup"),
        ("Small Business", "Small Business"),
        ("Enterprise", "Enterprise"),
        ("Personal Brand", "Personal Brand"),
        ("Portfolio Site", "Portfolio Site"),
        ("Other", "Other"),
    ]

    PACKAGE_CHOICES = [
        ("Starter", "Starter"),
        ("Growth", "Growth"),
        ("Premium", "Premium"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("reviewed", "Reviewed"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("rejected", "Rejected"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("paid", "Paid"),
        ("pending", "Pending"),
    ]

    project_id = models.CharField(
        max_length=5, unique=True, default=generate_project_id, editable=False,
        help_text="Unique 5-digit project identifier",
    )
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    business_name = models.CharField(max_length=200)
    business_type = models.CharField(max_length=50, choices=BUSINESS_TYPE_CHOICES)
    description = models.TextField(help_text="Description of the business")
    requirements = models.TextField(help_text="Website requirements and preferences")
    package = models.CharField(max_length=50, choices=PACKAGE_CHOICES, default="Starter")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    # Invoice
    invoice = models.FileField(upload_to="invoices/", blank=True, null=True, help_text="Downloadable invoice file")

    # Payment status
    payment_status = models.CharField(
        max_length=10, choices=PAYMENT_STATUS_CHOICES, default="pending",
    )

    # Progress
    progress_percentage = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Project completion percentage (0-100)",
    )

    # Admin remarks
    remarks = models.TextField(blank=True, default="", help_text="Admin remarks about the project")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Project Request"
        verbose_name_plural = "Project Requests"

    def __str__(self):
        return f"[{self.project_id}] {self.full_name} – {self.business_name} ({self.package})"


class ProgressScreenshot(models.Model):
    """Screenshots showing project progress, managed from admin."""
    project = models.ForeignKey(
        ProjectRequest, on_delete=models.CASCADE, related_name="screenshots",
    )
    image = models.ImageField(upload_to="progress_screenshots/")
    caption = models.CharField(max_length=255, blank=True, default="")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"Screenshot for [{self.project.project_id}] – {self.caption or 'No caption'}"


class ClientMessage(models.Model):
    """Messages between client and admin for a project."""
    project = models.ForeignKey(
        ProjectRequest, on_delete=models.CASCADE, related_name="messages",
    )
    sender = models.CharField(
        max_length=10,
        choices=[("client", "Client"), ("admin", "Admin")],
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"[{self.sender}] {self.project.project_id} – {self.message[:50]}"
