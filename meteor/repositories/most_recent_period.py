from core.mongodb import meteor_connection 
from datetime import datetime
from dateutil.relativedelta import relativedelta
from core.utils import parse_bson

class MostRecentPeriodRepository:
    def handle_data(self, coordinates):
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
            }
        }

        target_data = {
            'time': True
        }

        cursor_data = models.find(query_by_coordinates, target_data).sort({ 'time': -1 }).limit(1)

        data = parse_bson(cursor_data)


        to_date = datetime.fromisoformat(data[0]['time']['$date'].replace("Z", "+00:00"))

        from_date = to_date - relativedelta(months=6)

        return [from_date.strftime("%Y-%m-%d"), to_date.strftime("%Y-%m-%d")]

most_recent_period_repository = MostRecentPeriodRepository()