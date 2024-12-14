from rest_framework.views import APIView
from rest_framework.response import Response
from core.utils.jwt import decode_jwt

class DecodeTokenView(APIView):
    def post(self, request):
        token = request.data['token']

        payload = decode_jwt(token)

        return Response(payload)