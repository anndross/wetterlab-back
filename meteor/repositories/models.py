from core.mongodb import meteor_connection
from core.utils import parse_bson
import unicodedata
import math
import pandas as pd
from datetime import date
import numpy as np

class ModelsRepository:
    def __init__(self): 
        self.collection = meteor_connection.get_collection('models')

    def handle_data(self, coordinate, service, mean, ref_time): 
        max_distance = 1000

        query_by_coordinate = {
            'position': {
                '$near': {
                    '$geometry': {
                        'type': 'Point',
                        'coordinates': coordinate
                    },
                    '$maxDistance': max_distance
                }
            },
            'ref_time': ref_time
        }

        target_data = {
            service: {"$ifNull": [f"${service}", 0]},
            'time': True,
        }

        cursor_data = self.collection.find(query_by_coordinate, target_data).sort('time', 1)
        data = list(cursor_data)

        if len(data) == 0:
            return []

        service_value = f'{service}_value'

        df = pd.DataFrame(data)

        df['time'] = pd.to_datetime(df['time'])

        df[service_value] = pd.to_numeric(df[service].apply(lambda x: x), errors='coerce')        
        df[service_value].fillna(0, inplace=True)

        df['time'] = pd.to_datetime(df['time'])
        df.set_index('time', inplace=True)
        
        # mean_by_interval = df[service_value].resample(f'{mean}D').mean()
        
        # json_data = mean_by_interval.reset_index().rename(columns={'time': 'date', service_value: 'value', 'ref_time': 'ref_time'}).to_dict(orient='records')
        

        # Calculando estatísticas por intervalo de tempo
        resampled_stats = (
            df[service_value]
            .resample(f'{mean}D')
            .agg(['min', lambda x: np.percentile(x, 25), 'median', lambda x: np.percentile(x, 75), 'max'])
        )

        # Renomear as colunas resultantes
        resampled_stats.columns = ['min', 'p25', 'median', 'p75', 'max']

        # Resetando o índice para trazer 'datetime' como coluna
        resampled_stats.reset_index(inplace=True)

        dict_data = resampled_stats.rename(columns={'time': 'date'}).to_dict(orient='records')
        return dict_data

models_repository = ModelsRepository()