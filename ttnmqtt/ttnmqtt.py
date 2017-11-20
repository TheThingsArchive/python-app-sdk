# coding: Latin-1
# Copyright © 2017 The Things Network
# Use of this source code is governed by the
# MIT license that can be found in the LICENSE file.


import paho.mqtt.client as mqtt
from events import Events
import json
import base64
from collections import namedtuple
from .gRPCfiles import discovery_pb2_grpc
from .gRPCfiles import discovery_pb2
import grpc
import os

os.environ['GRPC_SSL_CIPHER_SUITES'] = ("ECDHE-ECDSA-AES256-"
                                        "GCM-SHA384:ECDHE-RSA-AES256-"
                                        "GCM-SHA384:ECDHE-ECDSA-CHACHA20-"
                                        "POLY1305:"
                                        "ECDHE-RSA-CHACHA20-POLY1305:"
                                        "ECDHE-ECDSA-AES128-GCM-SHA256:"
                                        "ECDHE-RSA-AES128-GCM-SHA256:"
                                        "ECDHE-ECDSA-AES256-SHA384:"
                                        "ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-"
                                        "AES128-SHA256:"
                                        "ECDHE-RSA-AES128-SHA256")


def _json_object_hook(d):
    return namedtuple('MSG', d.keys())(*d.values())


def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)


class DownlinkMessage:
    def __init__(self, port, confirmed=False, schedule=None):
        self.port = port
        if confirmed:
            self.confirmed = confirmed
        if schedule:
            self.schedule = schedule

    def obj2json(self):
        json_msg = json.dumps(self.__dict__)
        return str(json_msg)


class MyEvents(Events):
    __events__ = (
        "uplink_msg",
        "downlink_msg",
        "connect",
        "close")


class MQTTClient:

    def __init__(self, appID, appAccessKey, mqttAddress=""):
        self.__client = mqtt.Client()
        self.__appID = appID
        self.__accessKey = appAccessKey
        self.__events = MyEvents()
        self.__mqttAddress = mqttAddress
        self.ErrorMsg = ""
        try:
            self.connect()
            self.start()
        except:
            self.ErrorMsg = ("Connection failed: wrong appID,"
                             "accessKey or mqttAddress")

    def connect(self):
        self.__client.on_connect = self._onConnect()
        self.__client.on_publish = self._onDownlink()
        self.__client.on_message = self._onMessage()
        self.__client.on_disconnect = self._onClose()

        self.__client.username_pw_set(self.__appID, self.__accessKey)
        if self.__mqttAddress == "":
            creds = grpc.ssl_channel_credentials()
            channel = grpc.secure_channel(
                'discovery.thethings.network:1900',
                creds)
            stub = discovery_pb2_grpc.DiscoveryStub(channel)
            req = discovery_pb2.GetByAppIDRequest()
            req.app_id = self.__appID
            res = stub.GetByAppID(req)
            self.__mqttAddress = res.mqtt_address
            split = self.__mqttAddress.split(':')
            address = split[0]
            port = int(split[1])
            self.__client.connect(address, port, 60)
        else:
            split = self.__mqttAddress.split(':')
            address = split[0]
            port = int(split[1])
            self.__client.connect(address, port, 60)

    def _onConnect(self):
        def on_connect(client, userdata, flags, rc):
            if(rc == 0):
                client.subscribe('{}/devices/+/up'.format(self.__appID))
                res = True
            else:
                res = False
            if self.__events.connect:
                self.__events.connect(res, client=self)
        return on_connect

    def _onClose(self):
        def on_disconnect(client, userdata, rc):
            if rc != 0:
                self.ErrorMsg = "Unexpected Disconnection"
                res = False
            else:
                res = True
            if self.__events.close:
                self.__events.close(res, client=self)
        return on_disconnect

    def _onMessage(self):
        def on_message(client, userdata, msg):
            j_msg = str(json.dumps(json.loads(msg.payload.decode('utf-8'))))
            obj = json2obj(j_msg)
            if self.__events.uplink_msg:
                self.__events.uplink_msg(obj, client=self)
        return on_message

    def _onDownlink(self):
        def on_publish(client, userdata, mid):
            self.midCounter = mid
            if self.__events.downlink_msg:
                self.__events.downlink_msg(mid, client=self)
        return on_publish

    def set_uplink_callback(self, callback):
        self.__events.uplink_msg += callback

    def set_downlink_callback(self, callback):
        self.__events.downlink_msg += callback

    def set_connect_callback(self, callback):
        self.__events.connect += callback

    def set_close_callback(self, callback):
        self.__events.close += callback

    def start(self):
        self.__client.loop_start()

    def stop(self):
        self.__client.loop_stop()
        self.close()

    def close(self):
        self.__client.disconnect()
        self.connectFlag = 0

    def send(self, devID, pay, port=1, conf=False, sched="replace"):
        message = DownlinkMessage(port, conf, sched)
        if isinstance(pay, str):
            message.payload_raw = pay
        else:
            message.payload_fields = pay

        msg = message.obj2json()
        self.__client.publish(
            '{}/devices/{}/down'.format(self.__appID, devID),
            msg)
