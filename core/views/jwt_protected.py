from rest_framework.views import APIView
from core.utils import jwt_verify_decorator
from django.utils.decorators import method_decorator

class JWTProtectedView(APIView): 
    @method_decorator(jwt_verify_decorator)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
