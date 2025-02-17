from rest_framework.views import APIView
from rest_framework.response import Response
from setup.utils import parse_bson
from ..services.available_services import AvailableServicesService

class AvailableServices(APIView):
    def get(self, request):
        customer_id = request.query_params.get('customer_id')

        if customer_id is None:
            return Response({'error': 'O id é obrigatório'})

        available_services_service = AvailableServicesService(customer_id)

        coordinates = available_services_service.get_coordinates()

        return Response(coordinates)
