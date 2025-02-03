from setup.db import meteor_connection
from setup.utils import parse_bson
import pandas as pd
import numpy as np

class ModelsService:
    def __init__(self, coordinate, service, mean, ref_time):
        self.collection = meteor_connection.get_collection('models')
        self.ref_time = ref_time
        self.coordinate = coordinate
        self.service = service
        self.mean = mean
    
    def get_data_from_db(self):
        max_distance = 1000 # metros

        # Consulta geoespacial com filtro por ref_time
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
            'category': 0,
            'type': 1,
            'ref_time': self.ref_time
        }

        # Campos desejados na consulta
        projection = {
            self.service: {"$ifNull": [f"${self.service}", 0]},
            'time': 1,
            '_id': 0
        }

        # Recuperando dados do MongoDB
        cursor = self.collection.find(query, projection).sort('time', 1)
        data = list(cursor)

        return data

    def handle_data(self):
        data = self.get_data_from_db()

        if not data:
            return []

        # Transformando dados em DataFrame
        df = pd.DataFrame(data)
        df['time'] = pd.to_datetime(df['time'])
        df.set_index('time', inplace=True)

        # Garantindo que o campo do serviço seja numérico
        df[self.service] = pd.to_numeric(df[self.service], errors='coerce').fillna(0)

        # Resample e cálculo de estatísticas
        stats = df[self.service].resample(f'{self.mean}D').agg(
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
        result = stats.rename(columns={'time': 'date'}).to_dict(orient='records')
        return result

