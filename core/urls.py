from django.urls import path

from .views import ProjectRequestCreateView

app_name = "core"

urlpatterns = [
    path("project-requests/", ProjectRequestCreateView.as_view(), name="project-request-create"),
]
