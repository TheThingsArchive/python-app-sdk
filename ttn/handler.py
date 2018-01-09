# coding: Latin-1
# Copyright © 2018 The Things Network
# Use of this source code is governed by the
# MIT license that can be found in the LICENSE file.

from .application import ApplicationClient
from .ttnmqtt import MQTTClient
from .discovery import DiscoveryClient
from utils import stubs
import os

if os.getenv("GRPC_SSL_CIPHER_SUITES"):
    os.environ["GRPC_SSL_CIPHER_SUITES"] += os.pathsep + stubs.MODERN_CIPHER
else:
    os.environ["GRPC_SSL_CIPHER_SUITES"] = stubs.MODERN_CIPHER


class HandlerClient:

    def __init__(self, app_id,
                 app_access_key,
                 discovery_address=None,
                 certificate=None):
        self.app_id = app_id
        self.app_access_key = app_access_key
        self.discovery_address = discovery_address
        self.certificate = certificate
        self.open()

    def open(self):
        if not hasattr(self, 'announcement'):
            discovery = DiscoveryClient(self.discovery_address,
                                        self.certificate)
            self.announcement = discovery.get_by_app_id(self.app_id)

    def data(self):
        if not hasattr(self, "announcement"):
            raise RuntimeError("HandlerClient needs to be open before"
                               "it can create a data client.")

        return MQTTClient(self.app_id,
                          self.app_access_key,
                          mqtt_address=self.announcement.mqtt_address)

    def application(self):
        if not hasattr(self, "announcement"):
            raise RuntimeError("HandlerClient needs to be open"
                               "before it can create a data client.")
        return ApplicationClient(self.app_id,
                                 self.app_access_key,
                                 net_address=self.announcement.net_address,
                                 certificate=self.announcement.certificate)
