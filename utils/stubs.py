# coding: Latin-1
# Copyright © 2017 The Things Network
# Use of this source code is governed by the
# MIT license that can be found in the LICENSE file.


from jose import jwt, jws
from .read_key import read_key
import math
import binascii
import time
import os

MODERN_CIPHER_SUITES = ("ECDHE-ECDSA-AES256-GCM-SHA384:"
                        "ECDHE-RSA-AES256-GCM-SHA384:"
                        "ECDHE-ECDSA-CHACHA20-POLY1305:"
                        "ECDHE-RSA-CHACHA20-POLY1305:"
                        "ECDHE-ECDSA-AES128-GCM-SHA256:"
                        "ECDHE-RSA-AES128-GCM-SHA256:"
                        "ECDHE-ECDSA-AES256-SHA384:"
                        "ECDHE-RSA-AES256-SHA384:"
                        "ECDHE-ECDSA-AES128-SHA256:"
                        "ECDHE-RSA-AES128-SHA256")

uplink = {
  "dev_id": "guest",
  "port": 1,
  "counter": 5,
  "payload_raw": "AQ==",
  "payload_fields": {
    "led": True,
  },
  "metadata": {
    "time": "2016-09-14T14:19:20.272552952Z",
    "frequency": 868.1,
    "modulation": "LORA",
    "data_rate": "SF7BW125",
    "coding_rate": "4/5",
    "gateways": [{
      "eui": "B827EBFFFE87BD22",
      "timestamp": 1960494347,
      "time": "2016-09-14T14:19:20.258723Z",
      "rssi": -49,
      "snr": 9.5,
      "rf_chain": 1,
    }],
  },
}

claims = {
  "scope": [ "apps" ],
}

appClaims = {
  "scope": [ "apps:test" ],
  "iss": "local",
  "iat": int(math.floor(time.time() / 1000) - 60),
  "apps": {
    "test": [
      "settings",
      "devices",
      "delete",
    ],
  },
}

serverkey = read_key('.env/discovery/server.key')
token = jws.sign(claims, serverkey, algorithm="ES256")

apptest = {
  "appId": "test",
  "appEui": "0011223344556677",
  "accessKey": "local.12345678",
  "accessToken": jws.sign(appClaims, serverkey, algorithm="ES256"),
  "payloadFormat": "custom",
  "decoder": "",
  "converter": "",
  "validator": "",
  "encoder": "",
  "registerOnJoinAccessKey": "",
}

handler = {
  "id": "dev",
  "serviceName": "handler",
  "description": "",
  "url": "",
  "pb_public": False,
  "netAddress": "handler:1904",
  "publicKey": read_key(".env/handler/server.pub"),
  "certificate": read_key(".env/handler/server.cert"),
  "apiAddress": "http://handler:8084",
  "mqttAddress": "handler:1883",
  "amqpAddress": "handler:5672",
}

handlerAddress = "localhost:1904"
mqttAddress = "localhost:1883"

devicetest = {
    "description": "Description",
    "appEui": "0011223344556677",
    "devEui": "9988776655443322",
    "devAddr": "11223344",
    "nwkSKey": binascii.b2a_hex(os.urandom(16)).upper(),
    "appSKey": binascii.b2a_hex(os.urandom(16)).upper(),
    "appKey": binascii.b2a_hex(os.urandom(16)).upper(),
    "fCntUp": 10,
    "fCntDown": 11,
    "latitude": 100,
    "longitude": 200,
    "altitude": 300,
    "attributes": {
      "foo": "bar",
    },
    "disableFCntCheck": True,
    "uses32BitFCnt": True,
}

discovery = {
  "address": "localhost:1900",
  "certificate": read_key(".env/discovery/server.cert"),
}
