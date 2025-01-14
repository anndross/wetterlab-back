import jwt
from datetime import datetime, timezone, timedelta

TOKEN_KEY = "9b15e6ff0a7546e739dbe2c87c71d397"
DEFAULT_TOKEN_EXPIRATION = 30 # 30 days

def encode_jwt(payload):
    return jwt.encode({
        **payload,
        "exp": datetime.now(tz=timezone.utc) + timedelta(days=DEFAULT_TOKEN_EXPIRATION)}, 
        key=TOKEN_KEY,
        algorithm="HS256"
    )

def decode_jwt(encoded):
    return jwt.decode(encoded, key=TOKEN_KEY, algorithms="HS256")
    