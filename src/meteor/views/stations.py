from core.mongodb import meteor_connection
from rest_framework.views import APIView
from rest_framework.response import Response
from ..repositories.station import station_repository 
from core.utils import parse_coordinates 

class StationsView(APIView):

    def get(self, request):
        longitude = request.query_params.get('longitude')
        latitude = request.query_params.get('latitude')
        # The order matters! Long [1] - Lat [0]
        coordinates = parse_coordinates([longitude, latitude])

        if not coordinates[1] or not coordinates[0]:
            return Response(
                { 'message': '`latitude` and `longitude` is a required query parameter'},
                status=400
            )
        
        station = station_repository.get_station_geolocation(coordinates)

        if not station:
            return Response(
                { 'message': 'Station not found for the provided coordinate' },
                status=404
            )

        return Response(station)