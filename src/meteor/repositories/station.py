from core.mongodb import meteor_connection
from core.utils import parse_bson
import unicodedata
import math
import pandas as pd

class StationRepository:
    def __init__(self): 
        self.collection = meteor_connection.get_collection('stations')
        # self.collection.create_index([("position", "2dsphere")])

    def transform_string(self, string):
        # Remover acentos
        text_without_accent = ''.join(
            c for c in unicodedata.normalize('NFKD', string) 
            if unicodedata.category(c) != 'Mn'
        )
        # Converter para maiúsculas
        return text_without_accent.upper()

    def convert_none_nan_to_string(self, data):
        """Recorre o dicionário/listas e converte None e NaN para string."""
        if isinstance(data, dict):
            return {key: self.convert_none_nan_to_string(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.convert_none_nan_to_string(item) for item in data]
        elif data is None:
            return "None"
        elif isinstance(data, float) and (math.isnan(data) or math.isinf(data)):
            return str(data)  # Converte NaN e inf para string
        else:
            return data  # Mantém o valor original para outros tipos

    def handle_data(self, coordinates, date_from, date_to, service, mean): 
        max_distance = 1000

        query_by_coordinates = {
            'position': {
                '$near': {
                    '$geometry': {
                        'type': 'Point',
                        'coordinates': coordinates
                    },
                    '$maxDistance': max_distance
                }
            },
            'datetime': {
                '$gte': date_from,  # Data inicial (>=)
                '$lte': date_to     # Data final (<=)
            }
        }

        target_data = {
            service: True,
            'datetime': True
        }

        cursor_data = self.collection.find(query_by_coordinates, target_data).limit(5000).sort('datetime', 1)

        service_value = f'{service}_value'

        data = list(cursor_data)

        if len(data) == 0 or service not in data[0]: return []

        df = pd.DataFrame(data)
        
        df['datetime'] = pd.to_datetime(df['datetime'])

        df[service_value] = pd.to_numeric(df[service].apply(lambda x: x['value']), errors='coerce')        
        df[service_value].fillna(0, inplace=True)

        df.set_index('datetime', inplace=True)

        mean_by_interval = df[service_value].resample(f'{mean}D').mean()
        
        json_data = mean_by_interval.reset_index().rename(columns={'datetime': 'date', service_value: 'value'}).to_dict(orient='records')

        return json_data


station_repository = StationRepository()