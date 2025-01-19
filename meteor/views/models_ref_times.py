from rest_framework.views import Response, APIView
from ..services.models_ref_times import ModelsRefTimesService
from setup.utils import parse_coordinates 
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class ModelsRefTimes(APIView):        
    # @method_decorator(cache_page(86400)) # Cache por 1 dia

    def get(self, request):
        # TODO: adicionar validações e retornar status

        longitude = request.query_params.get('longitude')
        latitude = request.query_params.get('latitude')

        coordinate = parse_coordinates([longitude, latitude])

        models_ref_times_service = ModelsRefTimesService(coordinate)

        ref_times = models_ref_times_service.get_ref_times()
        # print(ref_times)

        return Response(ref_times)        
