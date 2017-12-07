# coding: Latin-1
# Copyright © 2017 The Things Network
# Use of this source code is governed by the
# MIT license that can be found in the LICENSE file.


from .is_token import is_token
from .read_key import read_key
from jose import jwt, jws


def test_is_token():
    key = read_key(".env/discovery/server.key")
    token = jws.sign({"hello": "hello"}, key, algorithm="ES256")
    assert is_token(token)
