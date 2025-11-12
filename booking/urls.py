from django.urls import path
from . import views

urlpatterns =[
    path('', views.index, name='index4'),
    path('book/', views.book_appointment, name='book_appointment'),
]