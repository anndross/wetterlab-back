from rest_framework.views import Request, Response, APIView
from datetime import datetime
from ..repositories.models_ref_times import models_ref_times_repository
from core.utils import parse_coordinates 
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class ModelsRefTimes(APIView):        
    @method_decorator(cache_page(86400)) # Cache por 1 dia

    def get(self, request: Request):
        # TODO: adicionar validações e retornar status

        longitude = request.query_params.get('longitude')
        latitude = request.query_params.get('latitude')

        coordinates = parse_coordinates([longitude, latitude])

        ref_times = models_ref_times_repository.handle_data(coordinates)

        return Response(ref_times)        
