# coding: Latin-1
# Copyright © 2017 The Things Network
# Use of this source code is governed by the
# MIT license that can be found in the LICENSE file.


import os
import time
import json
from ttn import MQTTClient as mqtt
from utils import stubs


def test_connect_disconnect():

    def connectcallback(res, client):
        print(res)
        assert res

    def closecallback(res, client):
        print(res)
        assert res

    ttn_client = mqtt(stubs.apptest['appId'],
                      stubs.apptest['accessKey'],
                      mqtt_address=stubs.mqttAddress)
    ttn_client.set_connect_callback(connectcallback)
    ttn_client.set_close_callback(closecallback)
    ttn_client.connect()
    time.sleep(2)
    ttn_client.close()


def test_uplink():

    def uplinkcallback(message, client):
        print(message)
        assert message.payload_raw == 'AQ=='

    ttn_client = mqtt(stubs.apptest['appId'],
                      stubs.apptest['accessKey'],
                      mqtt_address=stubs.mqttAddress)
    ttn_client.set_uplink_callback(uplinkcallback)
    ttn_client.connect()
    time.sleep(2)
    ttn_client._MQTTClient__client.publish(
        '{}/devices/guest/up'.format(stubs.apptest['appId']),
        json.dumps(stubs.uplink))
    time.sleep(2)
    ttn_client.close()


def test_connect_error():

    def connectcallback(res, client):
        print(res)
        assert res is False

    ttn_client = mqtt(stubs.apptest['appId'],
                      stubs.apptest['accessKey'],
                      mqtt_address='badAddress:5555')
    ttn_client.set_connect_callback(connectcallback)
    try:
        ttn_client.connect()
    except:
        ttn_client.close()


def test_downlink_payloadraw():

    def downlinkcallback(mid, client):
        print(mid)
        assert mid == 1

    ttn_client = mqtt(stubs.apptest['appId'],
                      stubs.apptest['accessKey'],
                      mqtt_address=stubs.mqttAddress)
    ttn_client.set_downlink_callback(downlinkcallback)
    ttn_client.connect()
    time.sleep(2)
    ttn_client.send('guest', "AQ==")
    time.sleep(2)
    ttn_client.close()


def test_downlink_payloadfields():

    def downlinkcallback(mid, client):
        print(mid)
        assert mid == 1

    ttn_client = mqtt(stubs.apptest['appId'],
                      stubs.apptest['accessKey'],
                      mqtt_address=stubs.mqttAddress)
    ttn_client.set_downlink_callback(downlinkcallback)
    ttn_client.connect()
    time.sleep(2)
    ttn_client.send("guest", {"field1": 1, "field2": 2})
    time.sleep(2)
    ttn_client.close()


def test_providing_all_downlink_options():

    def downlinkcallback(mid, client):
        print(mid)
        assert mid == 1

    ttn_client = mqtt(stubs.apptest['appId'],
                      stubs.apptest['accessKey'],
                      mqtt_address=stubs.mqttAddress)
    ttn_client.set_downlink_callback(downlinkcallback)
    ttn_client.connect()
    time.sleep(2)
    ttn_client.send('guest', "AQ==", 2, True, "first")
    time.sleep(2)
    ttn_client.close()
