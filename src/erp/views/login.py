from rest_framework.views import APIView
from rest_framework.response import Response
from json import loads, dumps
from core.mongodb import erp_connection
from core.utils import parse_bson_single
from core.utils.jwt import encode_jwt, decode_jwt


class LoginView(APIView):

    def post(self, request):
        if 'email' not in request.data:
            return Response({'error': 'the email field is mandatory'}, status=502)

        email = request.data['email']

        customers = erp_connection.get_collection('customers')

        found_customer = customers.find_one({'email': email})

        if found_customer is None:
            return Response({'message': 'user not found'}, status=202)
        else:
            found_customer_json = parse_bson_single(found_customer)
             
            token = encode_jwt(found_customer_json, 30)
            print(token)

            return Response({'message': 'user found', 'token': token}, status=200)