from rest_framework import serializers

from .models import ProjectRequest


class ProjectRequestSerializer(serializers.ModelSerializer):
    """Serializer for creating project requests from the frontend form."""

    class Meta:
        model = ProjectRequest
        fields = [
            "id",
            "full_name",
            "email",
            "mobile",
            "business_name",
            "business_type",
            "description",
            "requirements",
            "package",
            "status",
            "created_at",
        ]
        read_only_fields = ["id", "status", "created_at"]
