from .stations import StationsService 
from .models import ModelsService
from .models_ensemble import ModelsEnsembleService

class ForecastService:
  def __init__(self, ref_time, coordinate, service, mean):
        self.ref_time = ref_time
        self.coordinate = coordinate
        self.service = service
        self.mean = mean

  def get_forecast(self):
      models = self.get_models_data()
      models_ensemble = self.get_models_ensemble_data()

      if not models:
          raise ValueError("No models data available")

      dates = [model['date'] for model in models]
      stations_date_from, stations_date_to = models[0]['date'], models[-1]['date']

      stations = self.get_stations_data(date_from=stations_date_from, date_to=stations_date_to)

      return {
          'dates': dates,
          'stations': self.fill_data(dates=dates, data=stations),
          'models': models,
          'models_ensemble': self.fill_data(dates=dates, data=models_ensemble)
      }

  def fill_data(self, dates, data):
      data_len = len(data)

      if len(dates) <= data_len:
          return data

      # Preenchendo os dados restantes com valores padrão
      default_entry = {"min": 0, "p25": 0, "median": 0, "p75": 0, "max": 0}
      filled_data = [
          data[i] if i < data_len else {"date": dates[i], **default_entry}
          for i in range(len(dates))
      ]

      return filled_data

  def get_models_data(self):
      models_service = ModelsService(
          ref_time=self.ref_time,
          service=self.service,
          mean=self.mean,
          coordinate=self.coordinate
      )
      return models_service.handle_data()

  def get_stations_data(self, date_from, date_to):
      station_service = StationsService(
          coordinate=self.coordinate,
          date_from=date_from,
          date_to=date_to,
          service=self.service,
          mean=self.mean
      )
      return station_service.handle_data()

  def get_models_ensemble_data(self):
      models_ensemble_service = ModelsEnsembleService(
          ref_time=self.ref_time,
          service=self.service,
          mean=self.mean,
          coordinate=self.coordinate
      )
      return models_ensemble_service.handle_data()