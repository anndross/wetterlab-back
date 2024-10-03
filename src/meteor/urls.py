from django.contrib import admin
from django.urls import path

from .views import StationsView, Models

urlpatterns = [
    path('stations', StationsView.as_view()),
    path('models', Models.as_view()),
]
