from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from .emails import send_request_received_email
from .models import ClientMessage, ProjectRequest
from .serializers import (
    ClientLoginSerializer,
    ClientMessageCreateSerializer,
    ProjectPortalSerializer,
    ProjectRequestSerializer,
)


class ProjectRequestThrottle(AnonRateThrottle):
    """Limit submissions to 5 per minute per IP to prevent spam."""
    rate = "5/min"


class ProjectRequestCreateView(generics.CreateAPIView):
    """
    POST /api/project-requests/
    Accepts project request form data from the frontend.
    """
    queryset = ProjectRequest.objects.all()
    serializer_class = ProjectRequestSerializer
    throttle_classes = [ProjectRequestThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        send_request_received_email(serializer.instance)
        return Response(
            {"message": "Project request submitted successfully.", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )


class ClientLoginView(APIView):
    """
    POST /api/client-login/
    Client enters project_id + email to access their project portal.
    Returns full project data if credentials match.
    """
    throttle_classes = [ProjectRequestThrottle]

    def post(self, request):
        serializer = ClientLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        project_id = serializer.validated_data["project_id"]
        email = serializer.validated_data["email"]

        try:
            project = ProjectRequest.objects.prefetch_related(
                "screenshots", "messages"
            ).get(project_id=project_id, email=email)
        except ProjectRequest.DoesNotExist:
            return Response(
                {"error": "No project found with the given ID and email."},
                status=status.HTTP_404_NOT_FOUND,
            )

        data = ProjectPortalSerializer(project, context={"request": request}).data
        return Response(data, status=status.HTTP_200_OK)


class ProjectDetailView(APIView):
    """
    GET /api/project/<project_id>/?email=...
    Returns full project details for the given project_id and email combo.
    """

    def get(self, request, project_id):
        email = request.query_params.get("email")
        if not email:
            return Response(
                {"error": "Email query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            project = ProjectRequest.objects.prefetch_related(
                "screenshots", "messages"
            ).get(project_id=project_id, email=email)
        except ProjectRequest.DoesNotExist:
            return Response(
                {"error": "No project found with the given ID and email."},
                status=status.HTTP_404_NOT_FOUND,
            )

        data = ProjectPortalSerializer(project, context={"request": request}).data
        return Response(data, status=status.HTTP_200_OK)


class ClientMessageView(APIView):
    """
    POST /api/project/<project_id>/messages/
    Client sends a message for their project. Requires email in body.
    """
    throttle_classes = [ProjectRequestThrottle]

    def post(self, request, project_id):
        email = request.data.get("email")
        if not email:
            return Response(
                {"error": "Email is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            project = ProjectRequest.objects.get(project_id=project_id, email=email)
        except ProjectRequest.DoesNotExist:
            return Response(
                {"error": "No project found with the given ID and email."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ClientMessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ClientMessage.objects.create(
            project=project,
            sender="client",
            message=serializer.validated_data["message"],
        )
        return Response(
            {"message": "Message sent successfully."},
            status=status.HTTP_201_CREATED,
        )
