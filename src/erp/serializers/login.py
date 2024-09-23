from rest_framework import serializers 

class LoginSerializer(serializers.Serializer): 
    email = serializers.EmailField(
        required=True, 
        error_messages={
            'required': 'Authentication e-mail is required', 
            'invalid': 'Sent e-mail should be valid'
        }
    )