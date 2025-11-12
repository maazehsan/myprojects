
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index3"),
    path("login", views.login_view, name="login3"),
    path("logout", views.logout_view, name="logout3"),
    path("register", views.register, name="register3"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("following/", views.following, name="following"),
    path("api/posts/", views.posts_api, name="posts_api"),                    
    path("api/posts/<int:post_id>/", views.post_detail_api, name="post_detail_api"),
    path("api/posts/<int:post_id>/like/", views.like_toggle_api, name="like_toggle_api"),
    path("api/follow/<str:username>/", views.follow_toggle_api, name="follow_toggle_api"),
]
