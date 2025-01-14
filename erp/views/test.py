from rest_framework.views import APIView
from rest_framework.response import Response
from setup.views import JWTProtectedView

class TestView(JWTProtectedView):
    def get(self, request):
        return Response({'message': 'This is a protected view!'})