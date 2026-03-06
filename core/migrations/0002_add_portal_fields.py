import random
import string

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import core.models


def populate_project_ids(apps, schema_editor):
    """Assign unique 5-digit IDs to any existing ProjectRequest rows."""
    ProjectRequest = apps.get_model("core", "ProjectRequest")
    used_ids = set()
    for row in ProjectRequest.objects.all():
        while True:
            new_id = "".join(random.choices(string.digits, k=5))
            if new_id not in used_ids:
                break
        used_ids.add(new_id)
        row.project_id = new_id
        row.save(update_fields=["project_id"])


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        # Step 1: Add project_id as nullable, non-unique first
        migrations.AddField(
            model_name="projectrequest",
            name="project_id",
            field=models.CharField(
                default=core.models.generate_project_id,
                help_text="Unique 5-digit project identifier",
                max_length=5,
                editable=False,
            ),
            preserve_default=False,
        ),
        # Step 2: Populate existing rows with unique IDs
        migrations.RunPython(populate_project_ids, migrations.RunPython.noop),
        # Step 3: Now make it unique
        migrations.AlterField(
            model_name="projectrequest",
            name="project_id",
            field=models.CharField(
                default=core.models.generate_project_id,
                editable=False,
                help_text="Unique 5-digit project identifier",
                max_length=5,
                unique=True,
            ),
        ),
        # Add invoice field
        migrations.AddField(
            model_name="projectrequest",
            name="invoice",
            field=models.FileField(
                blank=True, help_text="Downloadable invoice file",
                null=True, upload_to="invoices/",
            ),
        ),
        # Add payment_status
        migrations.AddField(
            model_name="projectrequest",
            name="payment_status",
            field=models.CharField(
                choices=[("paid", "Paid"), ("pending", "Pending")],
                default="pending", max_length=10,
            ),
        ),
        # Add progress_percentage
        migrations.AddField(
            model_name="projectrequest",
            name="progress_percentage",
            field=models.PositiveIntegerField(
                default=0,
                help_text="Project completion percentage (0-100)",
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(100),
                ],
            ),
        ),
        # Add remarks
        migrations.AddField(
            model_name="projectrequest",
            name="remarks",
            field=models.TextField(
                blank=True, default="",
                help_text="Admin remarks about the project",
            ),
        ),
        # Create ProgressScreenshot model
        migrations.CreateModel(
            name="ProgressScreenshot",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="progress_screenshots/")),
                ("caption", models.CharField(blank=True, default="", max_length=255)),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                ("project", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="screenshots",
                    to="core.projectrequest",
                )),
            ],
            options={
                "ordering": ["-uploaded_at"],
            },
        ),
        # Create ClientMessage model
        migrations.CreateModel(
            name="ClientMessage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("sender", models.CharField(
                    choices=[("client", "Client"), ("admin", "Admin")],
                    max_length=10,
                )),
                ("message", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("project", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="messages",
                    to="core.projectrequest",
                )),
            ],
            options={
                "ordering": ["created_at"],
            },
        ),
    ]
