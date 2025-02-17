from django.core.mail import send_mail
from setup.db import erp_connection
from django.db import models
from django.contrib.auth.models import User
import uuid

class LoginService(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="email_code")
  code = models.UUIDField(default=uuid.uuid4, editable=False)
  created_at = models.DateTimeField(auto_now_add=True)
  is_used = models.BooleanField(default=False)

  def __init__(self, email):
    self.email = email
  def find_customer(self):
    customer = erp_connection.get_collection('customers').find_one({
      'email': self.email 
    })

    return customer
  
  def SendEmailCode(self, user):
    # Cria um novo código
    code_instance, created = self.objects.get_or_create(user=user)
    if not created:
        code_instance.code = uuid.uuid4()
        code_instance.is_used = False
        code_instance.save()

    # Envia o e-mail
    subject = "Seu código de autenticação"
    message = f"Olá {user.username},\n\nSeu código de autenticação é: {code_instance.code}"
    send_mail(subject, message, 'seu_email@gmail.com', [user.email])

  def is_valid(self):
      from datetime import timedelta
      from django.utils.timezone import now
      return not self.is_used and now() < self.created_at + timedelta(minutes=10)
