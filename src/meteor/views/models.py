from rest_framework.views import APIView
from rest_framework.response import Response
from ..repositories.models import models_repository
from datetime import datetime
from core.utils import parse_coordinates 

class Models(APIView):
    def get(self, request):
        longitude = request.query_params.get('longitude')
        latitude = request.query_params.get('latitude')

        location = request.query_params.get('location')

        date_from_array = request.query_params.get('from').split('-')
        date_to_array = request.query_params.get('to').split('-')

        date_from = datetime(int(date_from_array[0]), int(date_from_array[1]), int(date_from_array[2]))
        date_to = datetime(int(date_to_array[0]), int(date_to_array[1]), int(date_to_array[2]))

        # The order matters! Long [1] - Lat [0]
        coordinates = parse_coordinates([longitude, latitude])

        # if not coordinates[1] or not coordinates[0]:
        #     return Response(
        #         { 'message': '`latitude` and `longitude` is a required query parameter'},
        #         status=400
        #     )
        
        models = models_repository.test(coordinates, date_from, date_to, location) or []

        
        print('models---------------', models, date_from, date_to, '---------------models')

        return Response(models)

