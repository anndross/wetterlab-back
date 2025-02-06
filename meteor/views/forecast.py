from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from datetime import datetime
from setup.utils import parse_coordinates 
from ..services.forecast import ForecastService
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class Forecast(APIView):
    # @method_decorator(cache_page(86400))  # Cache por 1 dia
    def get(self, request):
        # Validação de parâmetros
        longitude = request.query_params.get('longitude')
        latitude = request.query_params.get('latitude')
        service = request.query_params.get('service')
        mean = request.query_params.get('mean')
        ref_time = request.query_params.get('ref-time')

        if not all([longitude, latitude, service, mean, ref_time]):
            raise ValidationError("Todos os parâmetros (longitude, latitude, service, mean, ref-time) são obrigatórios.")

        try:
            coordinate = parse_coordinates([longitude, latitude])
        except ValueError:
            raise ValidationError("Coordenadas inválidas fornecidas.")

        try:
            ref_time = datetime.strptime(ref_time, "%Y-%m-%d-%H-%M-%S")
        except ValueError:
            raise ValidationError("Formato de ref-time inválido. Use o formato YYYY-MM-DD-HH-MM-SS.")

        # Obtenção da previsão
        forecast_service = ForecastService(ref_time, coordinate, service, mean)
        forecast = forecast_service.get_forecast()

        return Response(forecast)
