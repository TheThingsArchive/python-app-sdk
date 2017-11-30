import is_token as tk
import read_key as rk
from jose import jwt, jws

def test_is_token():
    key = rk.read_key('.env/discovery/server.key')
    token = jws.sign({'hello': 'hello'}, key, algorithm='ES256')
    assert tk.is_token(token)
