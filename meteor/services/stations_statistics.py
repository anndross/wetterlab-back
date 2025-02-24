from setup.db import meteor_connection
import pandas as pd
import numpy as np

class StationsStatisticsService:
  def __init__(self, coordinate, date_from, date_to, service):
    self.collection = meteor_connection.get_collection("stations")

    self.coordinate = coordinate
    self.date_from = date_from
    self.date_to = date_to
    self.service = service

  def get_data_from_db(self):
    max_distance = 1000

    query = {
        'position': {
            '$near': {
                '$geometry': {
                    'type': 'Point',
                    'coordinates': self.coordinate
                },
                '$maxDistance': max_distance
            }
        },
        'datetime': {'$gte': self.date_from, '$lte': self.date_to}
    }


    # Campos desejados na consulta
    projection = {
      self.service: {"$ifNull": [f"${self.service}", {"quality": 0, "value": 0}]},
      'datetime': 1,
      '_id': 0
    }

    print(query, projection)

    # Consulta geoespacial com filtro por ref_time
    cursor = self.collection.find(query, projection).sort("datetime", 1)

    data = list(cursor)

    return data
  

  def handle_data(self):
    data = self.get_data_from_db()
    if not data:
      return []
    
    # Transformando os dados em DataFrame
    df = pd.DataFrame(data)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index('datetime', inplace=True)

    df[f'{self.service}_value'] = pd.to_numeric(
              df[self.service].apply(lambda x: x.get('value', 0)), errors='coerce'
          ).fillna(0)

    service_value_col = f'{self.service}_value'

    # Resample e cálculo de estatísticas
    stats = df[service_value_col].resample('30D').agg(
        [
            'min',
            lambda x: np.percentile(x, 25),
            'median',
            lambda x: np.percentile(x, 75),
            'max'
        ]
    )

    # Renomeando colunas para termos descritivos
    stats.columns = ['min', 'p25', 'median', 'p75', 'max']
    stats.reset_index(inplace=True)

    # Convertendo para formato de lista de dicionários
    result = stats.rename(columns={'datetime': 'date'}).to_dict(orient='records')
    return result
