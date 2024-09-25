from core.mongodb import meteor_connection
from rest_framework.views import APIView
from rest_framework.response import Response
from ..repositories.station import station_repository 
from core.utils import parse_coordinates 
from datetime import datetime

class StationsView(APIView):

    def get(self, request):
        longitude = request.query_params.get('longitude')
        latitude = request.query_params.get('latitude')


        date_from_array = request.query_params.get('from').split('-')
        date_to_array = request.query_params.get('to').split('-')


        date_from = datetime(int(date_from_array[0]), int(date_from_array[1]), int(date_from_array[2]))
        date_to = datetime(int(date_to_array[0]), int(date_to_array[1]), int(date_to_array[2]))


        # The order matters! Long [1] - Lat [0]
        coordinates = parse_coordinates([longitude, latitude])

        if not coordinates[1] or not coordinates[0]:
            return Response(
                { 'message': '`latitude` and `longitude` is a required query parameter'},
                status=400
            )
        
        stations = station_repository.test(coordinates, date_from, date_to) or []
        return Response(stations)
        station = station_repository.find_closest_station(coordinates)


        if not station:
            return Response(
                { 'message': 'Station not found for the provided coordinate' },
                status=404
            )

        return Response(station)