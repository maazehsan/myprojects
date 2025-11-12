from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index2"),
    path("login", views.login_view, name="login2"),
    path("logout", views.logout_view, name="logout2"),
    path("register", views.register, name="register2"),

    # API Routes
    path("emails", views.compose, name="compose"),
    path("emails/<int:email_id>", views.email, name="email"),
    path("emails/<str:mailbox>", views.mailbox, name="mailbox"),
    
    # urls for different views
    path("inbox", views.index, name="inbox2"),
    path("sent", views.index, name="sent"),
    path("archive", views.index, name="archive"),
    path("compose", views.index, name="compose"),
]
