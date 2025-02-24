from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from ..services.models import ModelsService
from datetime import datetime
from setup.utils import parse_coordinates 
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class Models(APIView):
    def get(self, request):
        # TODO: adicionar validações e retornar status

        lon = request.query_params.get('lon')
        lat = request.query_params.get('lat')

        service = request.query_params.get('service')
        mean = request.query_params.get('mean')

        ref_time = request.query_params.get('ref-time')

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

        models_service = ModelsService(coordinate, service, mean, ref_time)

        models = models_service.handle_data() or []

        return Response(models)

