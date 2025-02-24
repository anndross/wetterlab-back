from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from setup.utils import parse_coordinates 
from datetime import datetime
from meteor.services.models_statistics import ModelsStatisticsService
from rest_framework.response import Response

class ModelsStatistics(APIView):
  def get(self, request):
    ref_time = request.query_params.get('ref-time')

    lat = request.query_params.get('lat')
    lon = request.query_params.get('lon')

    service = request.query_params.get('service')

    if not all([lat, lon, service, ref_time]):
        raise ValidationError("Todos os parâmetros (lat, lon, service, ref-time) são obrigatórios.")

    try:
        coordinate = parse_coordinates([lon, lat])
    except ValueError:
        raise ValidationError("Coordenada fornecida inválida.")

    try:
        ref_time = datetime.strptime(ref_time, "%Y-%m-%d-%H-%M-%S")
    except ValueError:
        raise ValidationError("Formato de datas inválidos. Use o formato YYYY-MM-DD-HH-MM-SS.")

    models_statistics_service = ModelsStatisticsService(
       coordinate=coordinate, 
       ref_time=ref_time,
       service=service
    )

    # Obtenção da previsão
    models_statistics = models_statistics_service.handle_data()

    return Response(models_statistics)