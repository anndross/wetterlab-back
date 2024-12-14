from rest_framework import serializers 

class LoginSerializer(serializers.Serializer): 
    email = serializers.EmailField(
        required=True, 
        error_messages={
            'required': 'O email é obrigatório', 
            'invalid': 'O email deve ser válido'
        }
    )