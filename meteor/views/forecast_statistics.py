from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from datetime import datetime
from setup.utils import parse_coordinates, logger, InternalServerError
from ..services.forecast_statistics import ForecastStatisticsService
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class ForecastStatistics(APIView):
    @method_decorator(cache_page(86400))  # Cache por 1 dia

    def get(self, request):
        # Validação de parâmetros
        lon = request.query_params.get('lon')
        lat = request.query_params.get('lat')
        service = request.query_params.get('service')
        ref_time = request.query_params.get('ref-time')

        if not all([lon, lat, service, ref_time]):
            raise ValidationError("Todos os parâmetros (lat, lon, service, ref-time) são obrigatórios.")

        try:
            coordinate = parse_coordinates([lon, lat])
        except ValueError:
            raise ValidationError("Coordenada fornecida inválida.")

        try:
            ref_time = datetime.strptime(ref_time, "%Y-%m-%d-%H-%M-%S")
        except ValueError:
            raise ValidationError("Formato de ref-time inválido. Use o formato YYYY-MM-DD-HH-MM-SS.")

        try:
            forecast_service = ForecastStatisticsService(ref_time, coordinate, service)

            # Obtenção da previsão
            forecast = forecast_service.get_forecast()
        except Exception as e:
            logger.error(f"Erro no servidor: {str(e)}")
            raise InternalServerError(f"Erro interno no servidor: {str(e)}")

        return Response(forecast)
