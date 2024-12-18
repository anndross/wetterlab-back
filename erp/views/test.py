from rest_framework.views import APIView
from rest_framework.response import Response
from core.views import JWTProtectedView

class TestView(JWTProtectedView):
    def get(self, request):
        print('the user is ', request.context.get('user'))
        print('the token is ', request.context.get('jwt_token'))
        return Response({'message': 'This is a protected view!'})