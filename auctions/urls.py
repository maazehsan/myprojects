from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index1"),
    path("login", views.login_view, name="login1"),
    path("logout", views.logout_view, name="logout1"),
    path("register", views.register, name="register1"),
    path("create", views.create_listing, name="create"),
    path("listing/<int:id>", views.listing_page, name="listing"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("watchlist/<int:id>", views.toggle_watchlist, name="toggle_watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<str:name>", views.category, name="category"),
    path("closed/", views.closed_listings, name="closed"),
]
