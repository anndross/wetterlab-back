from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from setup.utils import parse_coordinates 
from datetime import datetime
from meteor.services.stations_statistics import StationsStatisticsService
from rest_framework.response import Response

class StationsStatisticsView(APIView):
  def get(self, request):
    date_from = request.query_params.get('date-from')
    date_to = request.query_params.get('date-to')

    lat = request.query_params.get('lat')
    lon = request.query_params.get('lon')

    service = request.query_params.get('service')


    if not all([lat, lon, service, date_from, date_to]):
        raise ValidationError("Todos os parâmetros (lon, lon, service, ref-time) são obrigatórios.")

    try:
        coordinate = parse_coordinates([lon, lat])
    except ValueError:
        raise ValidationError("Coordenada fornecida inválida.")

    try:
        date_from = datetime.strptime(date_from, "%Y-%m-%d-%H-%M-%S")
        date_to = datetime.strptime(date_to, "%Y-%m-%d-%H-%M-%S")
    except ValueError:
        raise ValidationError("Formato de datas inválidos. Use o formato YYYY-MM-DD-HH-MM-SS.")

    stations_statistics_service = StationsStatisticsService(
       coordinate=coordinate, 
       date_from=date_from,
       date_to=date_to,
       service=service
    )

    # Obtenção da previsão
    stations_statistics = stations_statistics_service.handle_data()

    return Response(stations_statistics)