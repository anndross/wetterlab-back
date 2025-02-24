from django.urls import path
from .views import Stations, Models, Forecast, ModelsRefTimes, ModelsEnsemble, StationsStatistics, ModelsStatistics, ForecastStatistics

urlpatterns = [
    path('forecast', Forecast.as_view()),
    path('models', Models.as_view()),
    path('models-ref-times', ModelsRefTimes.as_view()),
    path('models-ensemble', ModelsEnsemble.as_view()),
    path('stations', Stations.as_view()),
    path('stations-statistics', StationsStatistics.as_view()),
    path('models-statistics', ModelsStatistics.as_view()),
    path('forecast-statistics', ForecastStatistics.as_view()),
]
