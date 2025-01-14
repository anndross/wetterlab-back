from rest_framework.views import APIView
from rest_framework.response import Response
from ..services.models import ModelsService
from datetime import datetime
from setup.utils import parse_coordinates 
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class Models(APIView):
    def get(self, request):
        # TODO: adicionar validações e retornar status

        longitude = request.query_params.get('longitude')
        latitude = request.query_params.get('latitude')

        service = request.query_params.get('service')
        mean = request.query_params.get('mean')

        ref_time = request.query_params.get('ref-time')

        ref_time_array = request.query_params.get('ref-time').split('-')
        ref_time = datetime(int(ref_time_array[0]), int(ref_time_array[1]), int(ref_time_array[2]), int(ref_time_array[3]), int(ref_time_array[4]), int(ref_time_array[5]))

        # The order matters! Long [1] - Lat [0]
        coordinates = parse_coordinates([longitude, latitude])

        models_service = ModelsService(coordinates, service, mean, ref_time)

        models = models_service.handle_data() or []

        return Response(models)

