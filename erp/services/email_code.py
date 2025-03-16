import random
from django.core.cache import cache
from django.core.mail import send_mail

class EmailCodeService: 
  def __init__(self, email):
    self.email = email


  def send_code(self):
    # Gera um código aleatório de 6 dígitos
    code = str(random.randint(100000, 999999))
    
    # Armazena no Redis com expiração de 5 minutos (300 segundos)
    cache.set(f'code:{self.email}', code, timeout=300)
    
    # Envia o código por e-mail
    send_mail(
        'Seu código de autenticação',
        f'Seu código de acesso é: {code}',
        'noreply@wetterlab.com',
        [self.email],
        fail_silently=False,
    )
    
    return {'message': 'Código enviado com sucesso'}
  
  def verify_code(self, code_entered):
    # Recupera o código armazenado no Redis
    stored_code = cache.get(f'code:{self.email}')
    
    if stored_code and code_entered == stored_code:
        return {'message': 'Código válido'}
    else:
        return {'error': 'Código inválido ou expirado'}

