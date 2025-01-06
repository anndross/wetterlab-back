from core.mongodb import meteor_connection
from core.utils import parse_bson
import pandas as pd
import numpy as np

class StationRepository:
    def __init__(self): 
        self.collection = meteor_connection.get_collection('stations')
        # self.collection.create_index([("position", "2dsphere")])

    def handle_data(self, coordinates, date_from, date_to, service, mean): 
        max_distance = 1000

        query_by_coordinates = {
            'position': {
                '$near': {
                    '$geometry': {'type': 'Point', 'coordinates': coordinates},
                    '$maxDistance': max_distance
                }
            },
            'datetime': {'$gte': date_from, '$lte': date_to}
        }

        target_data = {service: {"$ifNull": [f"${service}", {"quality": 0, "value": 0}]}, 'datetime': True}

        cursor_data = self.collection.find(query_by_coordinates, target_data).sort('datetime', 1)
        data = list(cursor_data)

        if len(data) == 0:
            return []


        df = pd.DataFrame(data)
        df['datetime'] = pd.to_datetime(df['datetime'])

        service_value = f'{service}_value'
        df[service_value] = pd.to_numeric(df[service].apply(lambda x: x.get('value', 0)), errors='coerce').fillna(0)

        df['datetime'] = pd.to_datetime(df['datetime'])
        df.set_index('datetime', inplace=True)

        # Calculando estatísticas por intervalo de tempo
        resampled_stats = (
            df[service_value]
            .resample(f'{mean}D')
            .agg(['min', lambda x: np.percentile(x, 25), 'median', lambda x: np.percentile(x, 75), 'max'])
        )

        # Renomear as colunas resultantes
        resampled_stats.columns = ['min', 'p25', 'median', 'p95_rsr', 'max']

        # Resetando o índice para trazer 'datetime' como coluna
        resampled_stats.reset_index(inplace=True)

        dict_data = resampled_stats.to_dict(orient='records')

        return dict_data



station_repository = StationRepository()