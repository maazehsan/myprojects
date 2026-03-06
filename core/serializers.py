from rest_framework import serializers

from .models import ClientMessage, ProgressScreenshot, ProjectRequest


class ProjectRequestSerializer(serializers.ModelSerializer):
    """Serializer for creating project requests from the frontend form."""

    class Meta:
        model = ProjectRequest
        fields = [
            "id",
            "project_id",
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
        read_only_fields = ["id", "project_id", "status", "created_at"]


class ProgressScreenshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgressScreenshot
        fields = ["id", "image", "caption", "uploaded_at"]


class ClientMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientMessage
        fields = ["id", "sender", "message", "created_at"]
        read_only_fields = ["id", "created_at"]


class ProjectPortalSerializer(serializers.ModelSerializer):
    """Full project details for the client portal."""
    screenshots = ProgressScreenshotSerializer(many=True, read_only=True)
    messages = ClientMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ProjectRequest
        fields = [
            "id",
            "project_id",
            "full_name",
            "email",
            "business_name",
            "business_type",
            "description",
            "requirements",
            "package",
            "status",
            "invoice",
            "payment_status",
            "progress_percentage",
            "remarks",
            "screenshots",
            "messages",
            "created_at",
            "updated_at",
        ]


class ClientLoginSerializer(serializers.Serializer):
    """Validates client login with project_id and email."""
    project_id = serializers.CharField(max_length=5)
    email = serializers.EmailField()


class ClientMessageCreateSerializer(serializers.ModelSerializer):
    """For clients to send a new message."""
    class Meta:
        model = ClientMessage
        fields = ["message"]
