from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from .models import ProjectRequest
from .serializers import ProjectRequestSerializer


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
        return Response(
            {"message": "Project request submitted successfully.", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )
