from rest_framework.exceptions import APIException

class InternalServerError(APIException):
    status_code = 500
    default_detail = 'Erro interno no servidor.'
    default_code = 'internal_error'
