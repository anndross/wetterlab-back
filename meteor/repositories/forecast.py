from .stations import station_repository 
from .models import models_repository

class ForecastRepository:
  def __init__(self, ref_time, coordinate, service, mean):
    self.ref_time = ref_time
    self.coordinate = coordinate
    self.service = service
    self.mean = mean

    return
  
  def get_forecast(self): 
    models = self.get_models_data()
    print('models------------------------->', models)
    dates = list(map(lambda x: x['time'], models))

    stations_date_from = models[0]['time']
    stations_date_to = models[len(models) - 1]['time']

    stations = self.get_stations_data(date_from=stations_date_from, date_to=stations_date_to)
    print('stations------------------------->', stations)


    return {
      'dates': dates, 
      'stations': stations, 
      'models': models,
    }
  
  def fill_data(self, dates, data):
    data_len = len(data)

    if len(dates) <= data_len:
      return data

    def fill_in_remaining(index, datetime):
      if index < data_len:
        return data[index]
      
      return {
        "datetime": datetime,
        "min": 0,
        "p25": 0,
        "median": 0,
        "p95_rsr": 0,
        "max": 0
      }

    filled_data = map(fill_in_remaining, dates)

    return filled_data

  def get_models_data(self):
    models = models_repository.handle_data(ref_time=self.ref_time, service=self.service, mean=self.mean, coordinate=self.coordinate)

    mapped_data = [
        {
            "x": [],
            "y": []
        },
        {
            "x": [],
            "y": []
        },
        {
            "x": [],
            "y": []
        },
          {
            "x": [],
            "y": []
        },
        {
            "x": [],
            "y": []
        }
    ]

    for data in models: 
      mapped_data[0].x.append(data['time'])
      mapped_data[1].x.append(data['time'])
      mapped_data[2].x.append(data['time'])
      mapped_data[3].x.append(data['time'])
      mapped_data[4].x.append(data['time'])

      mapped_data[0].y.append(data['min'])
      mapped_data[1].y.append(data['p25'])
      mapped_data[2].y.append(data['median'])
      mapped_data[3].y.append(data['p75'])
      mapped_data[4].y.append(data['max'])

    return mapped_data
  
  def get_stations_data(self, date_from, date_to):
    stations = station_repository.handle_data(date_from, date_to, service=self.service, mean=self.mean, coordinate=self.coordinate)

    mapped_data = [
        {
            "x": [],
            "y": []
        },
        {
            "x": [],
            "y": []
        },
        {
            "x": [],
            "y": []
        },
          {
            "x": [],
            "y": []
        },
        {
            "x": [],
            "y": []
        }
    ]


    for data in stations: 
      mapped_data[0].x.append(data['datetime'])
      mapped_data[1].x.append(data['datetime'])
      mapped_data[2].x.append(data['datetime'])
      mapped_data[3].x.append(data['datetime'])
      mapped_data[4].x.append(data['datetime'])

      mapped_data[0].y.append(data['min'])
      mapped_data[1].y.append(data['p25'])
      mapped_data[2].y.append(data['median'])
      mapped_data[3].y.append(data['p75'])
      mapped_data[4].y.append(data['max'])

    return mapped_data
