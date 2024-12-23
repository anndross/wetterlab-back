from core.mongodb import meteor_connection

class ModelsRefTimesRepository:
    def handle_data(self, coordinates):
        models = meteor_connection.get_collection('models')

        max_distance = 1000

        pipeline = [
            {
                '$geoNear': {
                    'near': {
                        'type': 'Point',
                        'coordinates': coordinates
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
        reftimes = models.aggregate(pipeline)

        return list(reftimes)

models_ref_times_repository = ModelsRefTimesRepository()
