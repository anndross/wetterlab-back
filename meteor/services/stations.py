from setup.db import meteor_connection
import pandas as pd
import numpy as np

class StationsService:
    def __init__(self, coordinate, date_from, date_to, service, mean): 
        self.collection = meteor_connection.get_collection('stations')
        self.date_from = date_from
        self.date_to = date_to
        self.coordinate = coordinate
        self.service = service
        self.mean = mean

    def get_data_from_db(self):
        max_distance = 1000 # metros

        # Consulta geoespacial com intervalo de datas
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

        # Projeção de campos
        projection = {
            self.service: {"$ifNull": [f"${self.service}", {"quality": 0, "value": 0}]},
            'datetime': 1,
            '_id': 0
        }

        # Recuperando dados do MongoDB
        cursor = self.collection.find(query, projection).sort('datetime', 1)
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

        # Extraindo valores do serviço e garantindo que sejam numéricos
        df[f'{self.service}_value'] = pd.to_numeric(
            df[self.service].apply(lambda x: x.get('value', 0)), errors='coerce'
        ).fillna(0)

        service_value_col = f'{self.service}_value'

        # Calculando estatísticas por intervalo de tempo
        stats = df[service_value_col].resample(f'{self.mean}D').agg(
            [
                'median',
            ]
        )

        # Renomeando colunas para termos descritivos
        stats.columns = ['median']
        stats.reset_index(inplace=True)

        # Convertendo para formato de lista de dicionários
        result = stats.rename(columns={'datetime': 'date'}).to_dict(orient='records')
        return result