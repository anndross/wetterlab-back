from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from json import loads, dumps
from setup.db import erp_connection
from setup.utils import parse_bson
from setup.utils.jwt import encode_jwt, decode_jwt
from ..serializers import LoginSerializer

class LoginView(APIView):

    def post(self, request):
        login_serializer = LoginSerializer(data=request.data)

        if not login_serializer.is_valid():
            return Response({ "error": login_serializer.errors['email'][0] }, status=status.HTTP_400_BAD_REQUEST)

        customer = erp_connection.get_collection('customers').find_one({
            "email": login_serializer.validated_data.get('email')
        })

        if not customer: 
            return Response({ "error": "Não foi encontrado nenhum usuário com este email" }, status=status.HTTP_400_BAD_REQUEST)
       
        customer_json = parse_bson(customer)
        auth_token = encode_jwt(customer_json)

        return Response({
            "message": "Authenticated successfully", 
            "data": auth_token
        })
