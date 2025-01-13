from .stations import station_repository 
from .models import models_repository
from core.utils import parse_bson

class ForecastRepository:
  def __init__(self, ref_time, coordinate, service, mean):
    self.ref_time = ref_time
    self.coordinate = coordinate
    self.service = service
    self.mean = mean

  def get_forecast(self): 
    models = self.get_models_data()

    if not models:
      raise ValueError("No models data available")
  
    dates = list(map(lambda x: x['date'], models))

    stations_date_from = models[0]['date']
    stations_date_to = models[len(models) - 1]['date']

    stations = self.get_stations_data(date_from=stations_date_from, date_to=stations_date_to)

    return {
      'dates': dates, 
      'stations': self.fill_data(dates=dates, data=stations), 
      'models': models,
    }
  
  def fill_data(self, dates, data):
    data_len = len(data)

    if len(dates) <= data_len:
        return data

    def fill_in_remaining(datetime, index):
        if index < data_len:
            return data[index]
        return {
            "date": datetime,
            "min": 0,
            "p25": 0,
            "median": 0,
            "p75": 0,
            "max": 0
        }
    
    filled_data = [fill_in_remaining(dates[i], i) for i in range(len(dates))]


    return filled_data

  def get_models_data(self):
    models = models_repository.handle_data(ref_time=self.ref_time, service=self.service, mean=self.mean, coordinate=self.coordinate)

    return models
  
  def get_stations_data(self, date_from, date_to):
    stations = station_repository.handle_data(coordinate=self.coordinate, date_from=date_from, date_to=date_to, service=self.service, mean=self.mean)

    return stations
