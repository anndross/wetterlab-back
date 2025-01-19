from setup.db import meteor_connection

class ModelsRefTimesService:
    def __init__(self, coordinate):
        self.coordinate = coordinate

    def get_ref_times(self):
        models = meteor_connection.get_collection('models')

        max_distance = 1000

        pipeline = [
            {
                '$geoNear': {
                    'near': {
                        'type': 'Point',
                        'coordinates': self.coordinate
                    },
                    'distanceField': 'distance',
                    'maxDistance': max_distance,
                    'spherical': True
                }
            },
            {
                '$group': {
                    '_id': '$ref_time',  # Agrupa por `ref_time` para remover duplicados
                    'ref_time': { '$first': '$ref_time' }
                }
            },
            {
                '$sort': { 'ref_time': -1 }  # Ordena por `ref_time` de forma decrescente
            },
            {
                '$project': {
                    '_id': 0,
                    'value': {
                        '$dateToString': {
                            'format': '%Y-%m-%d-%H-%M-%S',
                            'date': '$ref_time'
                        }
                    },
                    'label': {
                        '$dateToString': {
                            'format': '%d/%m/%Y',
                            'date': '$ref_time'
                        }
                    }
                }
            }
        ]

        # Executa a pipeline de agregação
        ref_times = models.aggregate(pipeline)

        return list(ref_times)