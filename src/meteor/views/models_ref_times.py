from rest_framework.views import Request, Response, APIView
from datetime import datetime
from ..repositories.models_ref_times import models_ref_times_repository
from core.utils import parse_coordinates 

class ModelsRefTimes(APIView):        
    def get(self, request: Request):
        longitude = request.query_params.get('longitude')
        latitude = request.query_params.get('latitude')

        date_from_array = request.query_params.get('from').split('-')
        date_to_array = request.query_params.get('to').split('-')

        date_from = datetime(int(date_from_array[0]), int(date_from_array[1]), int(date_from_array[2]))
        date_to = datetime(int(date_to_array[0]), int(date_to_array[1]), int(date_to_array[2]))

        coordinates = parse_coordinates([longitude, latitude])

        ref_times = models_ref_times_repository.handle_data(coordinates, date_from, date_to)

        return Response(ref_times)        
