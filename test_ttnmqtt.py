# coding: Latin-1
# Copyright © 2018 The Things Network
# Use of this source code is governed by the
# MIT license that can be found in the LICENSE file.

import unittest
import time
import json
from ttn import MQTTClient as mqtt
from ttn.utils import stubs

MQTT_ADDR = "localhost:1883"

class TestMQTTClient(unittest.TestCase):

    def test_connect_disconnect(self):

        def connectcallback(res, client):
            print(res)
            assert res

        def closecallback(res, client):
            print(res)
            assert res

        ttn_client = mqtt(stubs.apptest["appId"],
                          stubs.apptest["accessKey"],
                          mqtt_address=MQTT_ADDR)
        ttn_client.set_connect_callback(connectcallback)
        ttn_client.set_close_callback(closecallback)
        ttn_client.connect()
        time.sleep(1)
        ttn_client.close()


    def test_uplink(self):

        def uplinkcallback(message, client):
            print(message)
            assert message.payload_raw == "AQ=="

        ttn_client = mqtt(stubs.apptest["appId"],
                          stubs.apptest["accessKey"],
                          mqtt_address=MQTT_ADDR)
        ttn_client.set_uplink_callback(uplinkcallback)
        ttn_client.connect()
        time.sleep(1)
        ttn_client._MQTTClient__client.publish(
            "{}/devices/guest/up".format(stubs.apptest["appId"]),
            json.dumps(stubs.uplink))
        time.sleep(1)
        ttn_client.close()


    def test_connect_error(self):

        def connectcallback(res, client):
            print(res)
            assert res is False

        ttn_client = mqtt(stubs.apptest["appId"],
                          stubs.apptest["accessKey"],
                          mqtt_address="badAddress:5555")
        ttn_client.set_connect_callback(connectcallback)
        try:
            ttn_client.connect()
        except:
            ttn_client.close()


    def test_downlink_payloadraw(self):

        def downlinkcallback(mid, client):
            print(mid)
            assert mid == 1

        ttn_client = mqtt(stubs.apptest["appId"],
                          stubs.apptest["accessKey"],
                          mqtt_address=MQTT_ADDR)
        ttn_client.set_downlink_callback(downlinkcallback)
        ttn_client.connect()
        time.sleep(1)
        ttn_client.send("guest", "AQ==")
        time.sleep(1)
        ttn_client.close()


    def test_downlink_payloadfields(self):

        def downlinkcallback(mid, client):
            print(mid)
            assert mid == 1

        ttn_client = mqtt(stubs.apptest["appId"],
                          stubs.apptest["accessKey"],
                          mqtt_address=MQTT_ADDR)
        ttn_client.set_downlink_callback(downlinkcallback)
        ttn_client.connect()
        time.sleep(1)
        ttn_client.send("guest", {"field1": 1, "field2": 2})
        time.sleep(1)
        ttn_client.close()


    def test_providing_all_downlink_options(self):

        def downlinkcallback(mid, client):
            print(mid)
            assert mid == 1

        ttn_client = mqtt(stubs.apptest["appId"],
                          stubs.apptest["accessKey"],
                          mqtt_address=MQTT_ADDR)
        ttn_client.set_downlink_callback(downlinkcallback)
        ttn_client.connect()
        time.sleep(1)
        ttn_client.send("guest", "AQ==", 2, True, "first")
        time.sleep(1)
        ttn_client.close()
