from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from ..services.models_ensemble import ModelsEnsembleService
from datetime import datetime
from setup.utils import parse_coordinates 

class ModelsEnsemble(APIView):
    def get(self, request):
        # TODO: adicionar validações e retornar status

        lon = request.query_params.get('lon')
        lat = request.query_params.get('lat')

        service = request.query_params.get('service')
        mean = request.query_params.get('mean')
        ref_time = request.query_params.get('ref-time')

        if not all([lon, lat, service, mean, ref_time]):
            raise ValidationError("Todos os parâmetros (lat, lon, service, mean, ref-time) são obrigatórios.")

        try:
            coordinate = parse_coordinates([lon, lat])
        except ValueError:
            raise ValidationError("Coordenada fornecida inválida.")

        try:
            ref_time = datetime.strptime(ref_time, "%Y-%m-%d-%H-%M-%S")
        except ValueError:
            raise ValidationError("Formato de ref-time inválido. Use o formato YYYY-MM-DD-HH-MM-SS.")


        models_service = ModelsEnsembleService(coordinate, service, mean, ref_time)

        models = models_service.handle_data() or []

        return Response(models)

