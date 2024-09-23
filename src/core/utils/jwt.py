import jwt
from datetime import datetime, timezone, timedelta

key = "9b15e6ff0a7546e739dbe2c87c71d397"


def encode_jwt(payload, days):
    encoded = jwt.encode({**payload, "exp": datetime.now(tz=timezone.utc) + timedelta(days=days)} , key, algorithm="HS256")

    return { "token": encoded }

def decode_jwt(encoded):
    decoded = jwt.decode(encoded, key, algorithms="HS256")

    return { "payload": decoded }