from core.mongodb import meteor_connection
from core.utils import parse_bson
import unicodedata

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

    def test(self, coordinates, date_from, date_to, location=None): 
        # stations = self.collection.find().limit(1000)
        # coordinates = [-47.9258346557617, -15.78944396972656]
        # coordinates = [-46.11916732788086, -17.78472137451172]
        # dist 100.000 - 2.74s
        # mindist 10.000 - 2.74s
        max_distance = 50000

        stations = []

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
                'datetime': {
                    '$gte': date_from,  # Data inicial (>=)
                    '$lte': date_to     # Data final (<=)
                }
            }

            stations = self.collection.find(query_by_coordinates).limit(50).sort('datetime', 1)
            stations = parse_bson(stations)

        else:
            query_by_location = {
                'location': self.transform_string(string=location),
                'datetime': {
                    '$gte': date_from,  # Data inicial (>=)
                    '$lte': date_to     # Data final (<=)
                }
            }

            stations = self.collection.find(query_by_location).limit(50).sort('datetime', 1)
            stations = parse_bson(stations)

        print('stations ->', stations, len(stations))
        # p = parse_bson(stations)
        # print('stations.len ->', len(p))

        return stations


    def get_stations(self, query, options): 
        query_cursor = self.collection.find(query)
        if options.get('limit'): query_cursor = query_cursor.limit(options.get('limit'))
        stations_parsed = parse_bson(query_cursor)
        return stations_parsed 

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

station_repository = StationRepository()

# from core.mongodb import meteor_connection
# from core.utils import parse_bson
# import math

# class StationRepository:
#     def __init__(self): 
#         self.collection = meteor_connection.get_collection('stations')

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

#     def filter_data_by_proximity(self, stations_data, lat_central, lon_central, raio_km):
#         # Função para filtrar os dados com base na proximidade a uma coordenada central
#         results = []

#         for data in stations_data:
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
# resultado_filtrado = filtrar_dados_por_proximidade(stations_data, lat_central, lon_central, raio_km)

# # Exibindo os resultados
    
    
# print(resultado_filtrado)
# station_repository = StationRepository()