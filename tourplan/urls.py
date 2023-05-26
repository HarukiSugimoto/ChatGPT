from django.urls import path

from . import views

app_name = "tourplan"
urlpatterns = [
    path("", views.search, name="search"),
]