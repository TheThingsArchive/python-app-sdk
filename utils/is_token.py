# coding: Latin-1
# Copyright © 2017 The Things Network
# Use of this source code is governed by the
# MIT license that can be found in the LICENSE file.


from jose import jwt
import read_key as rk

key = rk.read_key('.env/discovery/server.pub')

def is_token(string):
    try:
        return bool(jwt.decode(string, key))
    except:
        return False
