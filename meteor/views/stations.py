from setup.db import meteor_connection
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from ..services.stations import StationsService 
from setup.utils import parse_coordinates 
from datetime import datetime
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class Stations(APIView):
    def get(self, request):
        # TODO: adicionar validações e retornar status

        lon = request.query_params.get('lon')
        lat = request.query_params.get('lat')

        service = request.query_params.get('service')
        mean = request.query_params.get('mean')

        date_from = request.query_params.get('date-from')
        date_to = request.query_params.get('date-to')

        if not all([lon, lat, service, mean, date_from, date_to]):
            raise ValidationError("Todos os parâmetros (lat, lon, service, date-from, date-to) são obrigatórios.")

        try: 
            coordinate = parse_coordinates([lon, lat])
        except ValueError:
            raise ValidationError("Coordenada fornecida inválida.")

        try:
            date_from = datetime.strptime(date_from, "%Y-%m-%d-%H-%M-%S")
            date_to = datetime.strptime(date_to, "%Y-%m-%d-%H-%M-%S")
        except ValueError: 
            raise ValidationError("Formato de datas inválidos. Use o formato YYYY-MM-DD-HH-MM-SS.")

        stations_service = StationsService(coordinate, date_from, date_to, service, mean)

        stations = stations_service.handle_data() or []

        return Response(stations)