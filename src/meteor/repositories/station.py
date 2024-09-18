from core.mongodb import meteor_connection
from core.utils import parse_bson

class StationRepository:
    def __init__(self): 
        self.collection = meteor_connection.get_collection('stations')

    def get_stations(self, query, options): 
        query_cursor = self.collection.find(query)
        if options.get('limit'): query_cursor = query_cursor.limit(options.get('limit'))
        stations_parsed = parse_bson(query_cursor)
        return stations_parsed 
    
    def get_station_geolocation(self, coordinates): 
        max_coord_distance = 10000 # 10km
        query = {
            'position': {
                '$near': {
                    '$geometry': {
                        'type': 'Point', 
                        'coordinates': coordinates
                    }, 
                    '$maxDistance': max_coord_distance
                }
            }
        } 

        query_cursor = self.collection.find_one(query)

        if not query_cursor:
            return None

        station = parse_bson(query_cursor)
        return station

station_repository = StationRepository()