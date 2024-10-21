from core.mongodb import meteor_connection 
from datetime import datetime

class ModelsRefTimesRepository:
    def handle_data(self, coordinates, date_from, date_to):
        models = meteor_connection.get_collection('models')

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

        target_data = {
            'ref_time': True
        }

        cursor_data = models.find(query_by_coordinates, target_data).limit(5000).sort('ref_time')

        data = list(cursor_data)


        unique_dates = list({d['ref_time']: d for d in data}.values())
        
        sorted_ref_times = sorted(unique_dates, key=lambda x: x['ref_time'], reverse=True)
        
        reftimes = map(lambda x: { 'value': x['ref_time'].strftime('%Y-%m-%d-%H-%M-%S'), 'label': x['ref_time'].strftime('%d/%m/%Y') }, sorted_ref_times)

        return reftimes

models_ref_times_repository = ModelsRefTimesRepository()