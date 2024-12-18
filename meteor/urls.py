from django.contrib import admin
from django.urls import path

from .views import StationsView, Models, Forecast, ModelsRefTimes, MostRecentPeriod

urlpatterns = [
    path('stations', StationsView.as_view()),
    path('models', Models.as_view()),
    path('forecast', Forecast.as_view()),
    path('models-reftimes', ModelsRefTimes.as_view()),
    path('most-recent-period', MostRecentPeriod.as_view()),
]
