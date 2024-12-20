import hashlib
import uuid

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def generate_token(id : int) -> str:
    token = str(uuid.uuid4())
    token += f":{id}"
    return token

def get_id_from_token(token : str) -> int:
    return int(token.split(":")[-1])

def role_validate(expected, actual) -> bool:
    if actual == "admin":
        return True
    return actual == expected
    
