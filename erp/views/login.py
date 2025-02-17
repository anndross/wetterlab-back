from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from setup.utils import parse_bson
from setup.utils.jwt import encode_jwt
from ..serializers import LoginSerializer
from ..services.login import LoginService

class LoginView(APIView):

    def post(self, request):
        login_serializer = LoginSerializer(data=request.data)

        if not login_serializer.is_valid():
            return Response({ "error": login_serializer.errors['email'][0] }, status=status.HTTP_400_BAD_REQUEST)

        login_service = LoginService(login_serializer.validated_data.get('email'))
        
        customer = login_service.find_customer()

        if not customer: 
            return Response({ "error": "Não foi encontrado nenhum usuário com este email" }, status=status.HTTP_400_BAD_REQUEST)
       
        customer_json = parse_bson(customer)
        auth_token = encode_jwt(customer_json)

        return Response({
            "message": "Autenticado com sucesso!", 
            "data": auth_token
        })
