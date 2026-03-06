from django.urls import path

from .views import (
    ClientLoginView,
    ClientMessageView,
    ProjectDetailView,
    ProjectRequestCreateView,
)

app_name = "core"

urlpatterns = [
    path("project-requests/", ProjectRequestCreateView.as_view(), name="project-request-create"),
    path("client-login/", ClientLoginView.as_view(), name="client-login"),
    path("project/<str:project_id>/", ProjectDetailView.as_view(), name="project-detail"),
    path("project/<str:project_id>/messages/", ClientMessageView.as_view(), name="client-message"),
]
