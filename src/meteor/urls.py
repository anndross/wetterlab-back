from django.contrib import admin
from django.urls import path

from .views import StationsView

urlpatterns = [
    path('stations', StationsView.as_view()),
]
