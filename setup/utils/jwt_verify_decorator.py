from rest_framework.exceptions import AuthenticationFailed  
from setup.utils.jwt import decode_jwt 

# This is a custom decorator who should be used in a View method as described below
# from django.utils.decorators import method_decorator
# @method_decorator(jwt_verify)

def jwt_verify_decorator(view_handler):
    def _wrapped_view(request, *args, **kwargs): 
        auth_header = request.headers.get('Authorization')
        if not auth_header: 
            raise AuthenticationFailed('Authorization was not provided')

        jwt_token = auth_header.split('Bearer ')[1]
        if not jwt_token:
            raise AuthenticationFailed('JWT token was not provided')

        try: 
            user = decode_jwt(jwt_token)
            request.context = {
                'user': user, 
                'jwt_token': jwt_token
            }
        except: 
            raise AuthenticationFailed('Provided JWT Token is not valid')

        return view_handler(request, *args, **kwargs)
    return _wrapped_view