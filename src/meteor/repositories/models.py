from core.mongodb import meteor_connection
from core.utils import parse_bson
import unicodedata
import math

class ModelsRepository:
    def __init__(self): 
        self.collection = meteor_connection.get_collection('models')
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

    def test(self, coordinates, date_from, date_to, service): 
        max_distance = 1000

        models = []

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

        target_data = {
            service: True,
        }

        found_and_filtered_data = self.collection.find(query_by_coordinates, target_data).limit(200).sort('datetime', 1)

        models = self.convert_none_nan_to_string(parse_bson(found_and_filtered_data))
    
        return models

models_repository = ModelsRepository()