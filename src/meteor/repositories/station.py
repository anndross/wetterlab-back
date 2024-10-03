from core.mongodb import meteor_connection
from core.utils import parse_bson
import unicodedata
import math

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


    def test2(self, coordinates, date_from, date_to):
        print('coordinates', coordinates)

        target_latitude = coordinates[1]
        target_longitude = coordinates[0]


        geospatial_results = parse_bson(self.collection.find({
            'position': {
                '$near': {
                    '$geometry': {
                        'type': 'Point',
                        'coordinates': coordinates  # [longitude, latitude]
                    },
                    '$maxDistance': 1000  # Distância máxima em metros
                }
            },
            'datetime': {
                '$gte': date_from,  # Data inicial (>=)
                '$lte': date_to     # Data final (<=)
            }
        }).limit(50).sort('datetime', 1))

        print('geospatial_results', geospatial_results)

        # Verifique se resultados foram encontrados
        if geospatial_results:
            return geospatial_results

        # Se não houver resultados, extraia a parte inteira e a parte decimal
        integer_lat = int(target_latitude)
        decimal_lat = str(abs(target_latitude)).split('.')[1]  # Captura a parte decimal da latitude
        integer_long = int(target_longitude)
        decimal_long = str(abs(target_longitude)).split('.')[1]  # Captura a parte decimal da longitude

        # Cria listas de buscas com base nas partes decimais
        lat_searches = []
        long_searches = []
        
        # Procura pela parte decimal com menos precisão para a latitude
        for i in range(len(decimal_lat)):
            new_decimal = decimal_lat[:i] + '0' * (len(decimal_lat) - i)  # Completa com zeros
            new_latitude = float(f"{integer_lat}.{new_decimal}") * (-1 if target_latitude < 0 else 1)
            lat_searches.append(new_latitude)

        # Procura pela parte decimal com menos precisão para a longitude
        for i in range(len(decimal_long)):
            new_decimal = decimal_long[:i] + '0' * (len(decimal_long) - i)  # Completa com zeros
            new_longitude = float(f"{integer_long}.{new_decimal}") * (-1 if target_longitude < 0 else 1)
            long_searches.append(new_longitude)

        # Realiza a busca com as latitudes e longitudes geradas
        for lat_search in lat_searches:
            for long_search in long_searches:
                results = parse_bson(self.collection.find({
                    'position.coordinates.0': long_search,
                    'position.coordinates.1': lat_search,
                    'datetime': {
                        '$gte': date_from,  # Data inicial (>=)
                        '$lte': date_to     # Data final (<=)
                    }
                }).limit(50).sort('datetime', 1))
                if results:
                    return results

        return []


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

            stations = self.convert_none_nan_to_string(parse_bson(self.collection.find(query_by_coordinates).limit(50).sort('datetime', 1)))

            if len(stations) > 0:
                stations = parse_bson(stations)

        else:
            query_by_location = {
                'location': self.transform_string(string=location),
                'datetime': {
                    '$gte': date_from,  # Data inicial (>=)
                    '$lte': date_to     # Data final (<=)
                }
            }

            stations = self.convert_none_nan_to_string(parse_bson(self.collection.find(query_by_location).limit(50).sort('datetime', 1)))

            if len(stations) > 0:
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