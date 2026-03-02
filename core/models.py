from django.db import models


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

    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    business_name = models.CharField(max_length=200)
    business_type = models.CharField(max_length=50, choices=BUSINESS_TYPE_CHOICES)
    description = models.TextField(help_text="Description of the business")
    requirements = models.TextField(help_text="Website requirements and preferences")
    package = models.CharField(max_length=50, choices=PACKAGE_CHOICES, default="Starter")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Project Request"
        verbose_name_plural = "Project Requests"

    def __str__(self):
        return f"{self.full_name} – {self.business_name} ({self.package})"
