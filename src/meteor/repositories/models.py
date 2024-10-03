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

    def test(self, coordinates, date_from, date_to, location=None): 
        # models = self.collection.find().limit(1000)
        # coordinates = [-47.9258346557617, -15.78944396972656]
        # coordinates = [-46.11916732788086, -17.78472137451172]
        # dist 100.000 - 2.74s
        # mindist 10.000 - 2.74s
        max_distance = 20000

        models = []

        if location is None:
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

            models = self.convert_none_nan_to_string(parse_bson(self.collection.find(query_by_coordinates).limit(50).sort('time', 1)))

            # print('query_by_coordinates', query_by_coordinates, parse_bson(self.collection.find(query_by_location).limit(50).sort('time', 1)))
            
        else:
            query_by_location = {
                'location': self.transform_string(string=location),
                'time': {
                    '$gte': date_from,  # Data inicial (>=)
                    '$lte': date_to     # Data final (<=)
                }
            }

            # print('query_by_location', query_by_location, parse_bson(self.collection.find(query_by_location).limit(50).sort('time', 1)))
            models = self.convert_none_nan_to_string(parse_bson(self.collection.find(query_by_location).limit(50).sort('time', 1)))

        # print('models ->', models, len(models))
        # p = parse_bson(models)
        # print('models.len ->', len(p))

        return parse_bson(models)


    def get_models(self, query, options): 
        query_cursor = self.collection.find(query)
        if options.get('limit'): query_cursor = query_cursor.limit(options.get('limit'))
        models_parsed = parse_bson(query_cursor)
        return models_parsed 

    def get_station_by_exact_coordinates(self, coordinates):
        # Tenta buscar uma estação pela coordenada exata

        query = {
            'position.coordinates': coordinates
        }
        result = self.collection.find_one(query)
        return result

    def get_nearest_station(self, coordinates, max_distance):
        # Tenta buscar a estação mais próxima dentro de um raio especificado

        query = {
            'position': {
                '$near': {
                    '$geometry': {
                        'type': 'Point',
                        'coordinates': coordinates
                    },
                    '$maxDistance': max_distance
                }
            }
        }
        result = self.collection.find_one(query)
        return result


    def get_all_by_coordinates(self, coordinates):
        # Retorna todas as estações que possuem as mesmas coordenadas de uma estação encontrada

        query = {
            'position.coordinates': coordinates
        }

        return parse_bson(self.collection.find(query).limit(10))

    def find_closest_station(self, coordinates, starting_radius=1000, increment_radius=5000, max_radius=25000):
        # Algoritmo recursivo para buscar a estação mais próxima

        # 1. Busca exata
        exact_match = self.get_station_by_exact_coordinates(coordinates)

        if exact_match:
            # Se encontrar uma correspondência exata, retorna todas as estações com a mesma coordenada
            return self.get_all_by_coordinates(exact_match['position']['coordinates'])
        
        # 2. Busca próxima com raio crescente
        current_radius = starting_radius
        while current_radius <= max_radius:
            nearest_station = self.get_nearest_station(coordinates, current_radius)
            if nearest_station:
                # Se encontrar uma estação próxima, retorna todas as estações com a mesma coordenada
                return self.get_all_by_coordinates(nearest_station['position']['coordinates'])
            current_radius += increment_radius
        
        # 3. Se não encontrar nenhuma estação, retorna None ou uma mensagem
        return None

models_repository = ModelsRepository()

# from core.mongodb import meteor_connection
# from core.utils import parse_bson
# import math

# class StationRepository:
#     def __init__(self): 
#         self.collection = meteor_connection.get_collection('models')

#     def calculate_distance_haversine(self, lat1, lon1, lat2, lon2):
#         # Raio médio da Terra em quilômetros
#         R = 6371.0

#         # Converter de graus para radianos
#         lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

#         # Diferenças das coordenadas
#         dlat = lat2 - lat1
#         dlon = lon2 - lon1

#         # Fórmula de Haversine
#         a = math.sin(dlat / 2)*2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)*2
#         c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

#         # Distância
#         distancia = R * c
#         return distancia

#     def filter_data_by_proximity(self, models_data, lat_central, lon_central, raio_km):
#         # Função para filtrar os dados com base na proximidade a uma coordenada central
#         results = []

#         for data in models_data:
#             lon, lat = data['position']['coordinates'][1], data['position']['coordinates'][0]
#             distancia = self.calculate_distance_haversine(lat_central, lon_central, lat, lon)

#             if distancia <= raio_km:
#                 results.append(data)

#         return results

# # Coordenada central e raio em quilômetros
# lat_central = -46.2565  # Exemplo: Brasília
# lon_central = -22
# raio_km = 500  # Raio de 500 km

# # Chamando a função para filtrar os dados
# resultado_filtrado = filtrar_dados_por_proximidade(models_data, lat_central, lon_central, raio_km)

# # Exibindo os resultados
    
    
# print(resultado_filtrado)
# station_repository = StationRepository()