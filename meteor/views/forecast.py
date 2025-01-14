from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from setup.utils import parse_coordinates 
from ..services.forecast import ForecastService
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class Forecast(APIView):
    @method_decorator(cache_page(86400)) # Cache por 1 dia

    def get(self, request):
        # TODO: adicionar validações e retornar status

        # parâmetros
        longitude = request.query_params.get('longitude')
        latitude = request.query_params.get('latitude')
        coordinate = parse_coordinates([longitude, latitude])

        service = request.query_params.get('service')
        mean = request.query_params.get('mean')
    
        ref_time = request.query_params.get('ref-time')
        ref_time_array = request.query_params.get('ref-time').split('-')
        ref_time = datetime(int(ref_time_array[0]), int(ref_time_array[1]), int(ref_time_array[2]), int(ref_time_array[3]), int(ref_time_array[4]), int(ref_time_array[5]))

        forecast_repository = ForecastService(ref_time, coordinate, service, mean)
        forecast = forecast_repository.get_forecast()
        
        return Response(forecast)