import os
import time
import json
from ttnmqtt import MQTTClient as mqtt

appID = "guest"
accessKey = "guest"
mqttAddress = "localhost:1883"

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


def test_connect_disconnect():

    def connectcallback(res, client):
        print(res)
        assert res

    def closecallback(res, client):
        print(res)
        assert res

    ttn_client = mqtt(appID, accessKey, mqttAddress)
    ttn_client.set_connect_callback(connectcallback)
    ttn_client.set_close_callback(closecallback)
    time.sleep(2)
    ttn_client.stop()


def test_uplink():

    def uplinkcallback(message, client):
        print(message)
        assert message.payload_raw == 'AQ=='

    ttn_client = mqtt(appID, accessKey, mqttAddress)
    ttn_client.set_uplink_callback(uplinkcallback)
    time.sleep(2)
    ttn_client._MQTTClient__client.publish(
        'guest/devices/guest/up',
        json.dumps(uplink))
    time.sleep(2)
    ttn_client.stop()


def test_connect_error():

    ttn_client = mqtt(appID, accessKey, 'badAddress:5555')
    ttn_client.close()
    print(ttn_client.ErrorMsg)
    assert ttn_client.ErrorMsg == ("Connection failed: wrong appID,"
                                   "accessKey or mqttAddress")


def test_downlink_payloadraw():

    def downlinkcallback(mid, client):
        print(mid)
        assert mid == 2

    ttn_client = mqtt(appID, accessKey, mqttAddress)
    ttn_client.set_downlink_callback(downlinkcallback)
    time.sleep(2)
    ttn_client.send('guest', "AQ==")
    time.sleep(2)
    ttn_client.stop()


def test_downlink_payloadfields():

    def downlinkcallback(mid, client):
        print(mid)
        assert mid == 2

    ttn_client = mqtt(appID, accessKey, mqttAddress)
    ttn_client.set_downlink_callback(downlinkcallback)
    time.sleep(2)
    ttn_client.send('guest', {"field1": 1, "field2": 2})
    time.sleep(2)
    ttn_client.stop()


def test_providing_all_downlink_options():

    def downlinkcallback(mid, client):
        print(mid)
        assert mid == 2

    ttn_client = mqtt(appID, accessKey, mqttAddress)
    ttn_client.set_downlink_callback(downlinkcallback)
    time.sleep(2)
    ttn_client.send('guest', "AQ==", 2, True, "first")
    time.sleep(2)
    ttn_client.stop()
