from rest_framework.views import Response, APIView
from rest_framework.exceptions import ValidationError
from ..services.models_ref_times import ModelsRefTimesService
from setup.utils import parse_coordinates 
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class ModelsRefTimes(APIView):        
    @method_decorator(cache_page(86400)) # Cache por 1 dia

    def get(self, request):
        lon = request.query_params.get('lon')
        lat = request.query_params.get('lat')
        
        if not all([lat, lon]):
            raise ValidationError("Todos os parâmetros (lat, lon) são obrigatórios.")

        try:
            coordinate = parse_coordinates([lon, lat])
        except ValueError:
            raise ValidationError("Coordenada fornecida inválida.")

        models_ref_times_service = ModelsRefTimesService(coordinate)

        ref_times = models_ref_times_service.get_ref_times()

        return Response(ref_times)        
