from django.urls import path

from planner import views

urlpatterns = [
    path("locations/", views.list_locations, name="list_locations"),
]
