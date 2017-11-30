from jose import jwt
import read_key as rk

key = rk.read_key('.env/discovery/server.pub')

def is_token(string):
    try:
        return bool(jwt.decode(string, key))
    except:
        return False
