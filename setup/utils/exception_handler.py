from .logger import logger
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """ Captura todas as exceções do Django REST Framework e loga automaticamente. """
    
    # Chama o handler padrão do DRF para obter a resposta padrão
    response = exception_handler(exc, context)

    # Loga os erros automaticamente
    if response is not None:
        view = context.get('view', None)
        request = context.get('request', None)

        logger.error(
            f"Erro na view {view.__class__.__name__} - {request.method} {request.path}: {str(exc)}",
            exc_info=True  # Inclui o traceback completo no log
        )

    return response
