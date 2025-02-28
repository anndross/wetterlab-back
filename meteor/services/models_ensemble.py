from setup.db import meteor_connection
from setup.utils import parse_bson
import pandas as pd
import numpy as np

class ModelsEnsembleService:
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
            'tag': 'ensemble',
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

        df = pd.DataFrame(data)
        df['time'] = pd.to_datetime(df['time'])
        df.set_index('time', inplace=True)

        def get_x_value(x, type):
            return x.get(type, 0) if x and hasattr(x, 'get') else 0

        # Criando colunas com os valores existentes no banco
        df['min'] = df[self.service].apply(lambda x: get_x_value(x, "min"))
        df['p25'] = df[self.service].apply(lambda x: get_x_value(x, "p25"))
        df['median'] = df[self.service].apply(lambda x: get_x_value(x, "avg"))  # Supondo que 'avg' seja a mediana
        df['p75'] = df[self.service].apply(lambda x: get_x_value(x, "p75"))
        df['max'] = df[self.service].apply(lambda x: get_x_value(x, "max"))

        # Removendo a coluna original do serviço, pois agora temos os valores extraídos
        df.drop(columns=[self.service], inplace=True)

        # Resample mantendo as estatísticas existentes e calculando médias no período definido
        stats = df.resample(f'{self.mean}D').mean()

        # Resetando índice e renomeando coluna de tempo
        stats.reset_index(inplace=True)
        stats.rename(columns={'time': 'date'}, inplace=True)

        # Convertendo para lista de dicionários
        result = stats.to_dict(orient='records')
        print('result', result)
        return result

