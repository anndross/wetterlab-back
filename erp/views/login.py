from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from setup.utils import parse_bson
from setup.utils.jwt import encode_jwt
from ..serializers import LoginSerializer
from ..services.login import LoginService
from rest_framework.exceptions import ValidationError

class LoginView(APIView):

    def post(self, request):
        try:
            login_serializer = LoginSerializer(data=request.data)
        except Exception:
            raise ValidationError(detail={ "error": login_serializer.errors['email'][0] }, code=status.HTTP_400_BAD_REQUEST)


        if not login_serializer.is_valid():
            return Response({ "error": login_serializer.errors['email'][0] }, status=status.HTTP_400_BAD_REQUEST)

        try:
            login_service = LoginService(login_serializer.validated_data.get('email'))
            customer = login_service.find_customer()
        except Exception: 
            raise ValidationError(detail={ "error": "Não foi encontrado nenhum usuário com este email" }, code=status.HTTP_400_BAD_REQUEST)

        if not customer: 
            return Response({ "error": "Não foi encontrado nenhum usuário com este email" }, status=status.HTTP_400_BAD_REQUEST)
       
        try:
            customer_json = parse_bson(customer)
            auth_token = encode_jwt(customer_json)        
        except Exception:
            raise ValidationError(detail={ "error": "Não foi encontrado nenhum usuário com este email" }, code=status.HTTP_400_BAD_REQUEST)

        return Response({
            "message": "Autenticado com sucesso!", 
            "data": auth_token
        })
