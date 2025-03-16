from rest_framework.views import APIView
from rest_framework.response import Response
from services.email_code import EmailCodeService

class SendEmailCode(APIView):
  def post(self, request):
    data = request.data



