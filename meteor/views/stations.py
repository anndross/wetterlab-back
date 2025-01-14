from setup.db import meteor_connection
from rest_framework.views import APIView
from rest_framework.response import Response
from ..services.stations import StationsService 
from setup.utils import parse_coordinates 
from datetime import datetime
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class StationsView(APIView):
    def get(self, request):
        # TODO: adicionar validações e retornar status

        longitude = request.query_params.get('longitude')
        latitude = request.query_params.get('latitude')

        service = request.query_params.get('service')
        mean = request.query_params.get('mean')

        date_from_array = request.query_params.get('from').split('-')
        date_to_array = request.query_params.get('to').split('-')

        date_from = datetime(int(date_from_array[0]), int(date_from_array[1]), int(date_from_array[2]))
        date_to = datetime(int(date_to_array[0]), int(date_to_array[1]), int(date_to_array[2]))
        # The order matters! Long [1] - Lat [0]
        coordinates = parse_coordinates([longitude, latitude])

        stations_service = StationsService(coordinates, date_from, date_to, service, mean)

        stations = stations_service.handle_data() or []

        return Response(stations)