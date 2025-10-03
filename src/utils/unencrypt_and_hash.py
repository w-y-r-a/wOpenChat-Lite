import bcrypt
import base64

def unecrypt_and_hash(data: bytes) -> str: 
    to_bytes = base64.b64decode(data)
    unencrypted = to_bytes.decode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(unencrypted.encode(), salt).decode()
