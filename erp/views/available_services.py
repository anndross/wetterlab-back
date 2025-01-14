from rest_framework.views import APIView
from rest_framework.response import Response
from setup.db import erp_connection
from setup.utils import parse_bson

class AvailableServices(APIView):
    def get(self, request):
        production = erp_connection.get_collection('production')

        customer_id = request.query_params.get('customer_id')

        if customer_id is None:
            return Response({'error': 'O id é obrigatório'})

        # if not type(customer_id) is int:
        #     return Response({'error': 'O id deve ser um número'})

        query = {
            'customer_id': int(customer_id)
        }

        production_data_by_customer_id = production.find_one(query)

        production_data_by_customer_id = list(map(lambda x: list(reversed(x)), production_data_by_customer_id['services'][0]['locations']))



        return Response(parse_bson(production_data_by_customer_id))
