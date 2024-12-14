from rest_framework.views import Request, Response, APIView
from datetime import datetime
from ..repositories.most_recent_period import most_recent_period_repository
from core.utils import parse_coordinates 

class MostRecentPeriod(APIView):        
    def get(self, request: Request):
        longitude = request.query_params.get('longitude')
        latitude = request.query_params.get('latitude')

        coordinates = parse_coordinates([longitude, latitude])

        most_recent_period = most_recent_period_repository.handle_data(coordinates)

        return Response(most_recent_period)        
