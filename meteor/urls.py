from django.contrib import admin
from django.urls import path

from .views import StationsView, Models, Forecast, ModelsRefTimes, ModelsEnsemble, StationsStatisticsView

urlpatterns = [
    path('forecast', Forecast.as_view()),
    path('models', Models.as_view()),
    path('models-ref-times', ModelsRefTimes.as_view()),
    path('models-ensemble', ModelsEnsemble.as_view()),
    path('stations', StationsView.as_view()),
    path('stations-statistics', StationsStatisticsView.as_view()),
]
