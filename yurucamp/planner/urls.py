from django.urls import path

from planner import views

urlpatterns = [
    path("", views.trips_handler, name="trips"),
    path("locations/", views.list_locations, name="list_locations"),
    path("weather-check/", views.weather_check, name="weather_check"),
]
