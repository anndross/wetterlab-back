from core.mongodb import meteor_connection
from core.utils import parse_bson
import unicodedata
import math
import pandas as pd
from datetime import date

class ModelsRepository:
    def __init__(self): 
        self.collection = meteor_connection.get_collection('models')
        # self.collection.create_index([("position", "2dsphere")])

    def handle_data(self, coordinates, date_from, date_to, service, mean, reftime): 
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
            'time': {
                '$gte': date_from,  # Data inicial (>=)
                '$lte': date_to     # Data final (<=)
            }
        }

        if isinstance(reftime, date): 
            query_by_coordinates['ref_time'] = reftime


        print(reftime, query_by_coordinates)

        target_data = {
            service: True,
            'time': True,
        }

        cursor_data = self.collection.find(query_by_coordinates, target_data).sort('time', 1)

        service_value = f'{service}_value'
        def verify_if_service_data_exists(data):
            if service in data:
                return data
            else:
                data[service] = 0
                return data

        data = list(map(verify_if_service_data_exists, list(cursor_data)))


        if len(data) == 0: return []

        df = pd.DataFrame(data)
        df['time'] = pd.to_datetime(df['time'])

        df[service_value] = pd.to_numeric(df[service].apply(lambda x: x), errors='coerce')        
        df[service_value].fillna(0, inplace=True)

        df.set_index('time', inplace=True)
        
        mean_by_interval = df[service_value].resample(f'{mean}D').mean()
        
        json_data = mean_by_interval.reset_index().rename(columns={'time': 'date', service_value: 'value', 'ref_time': 'ref_time'}).to_dict(orient='records')

        return json_data

models_repository = ModelsRepository()