from django.urls import path
from .views import weather_view
from . import views

urlpatterns = [
    path('', weather_view, name='weather'),
    path('', views.weather_view, name='home'), 
    path('favorites/', views.favorite_locations, name='favorite_locations'),
    path('favorites/add/', views.add_favorite_location, name='add_favorite_location'),
    path('favorites/remove/<int:pk>/', views.remove_favorite_location, name='remove_favorite_location'),
]