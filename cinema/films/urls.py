from django.urls import path
from . import views

app_name = 'films'

urlpatterns = [
    path('mainpage/', views.mainpage, name='mainpage'),
    path('films_view/', views.films_view, name='films_view'),
    path('reviews/', views.reviews, name='reviews'),
    path('add_review/', views.add_review, name='add_review'),
    path('list/', views.list, name='list'),
    path('add/', views.add, name='add'),
    path('delete/', views.delete, name='delete'),
    path("signup/", views.SignUp.as_view(), name="signup")
]