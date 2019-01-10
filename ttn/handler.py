# coding: Latin-1
# Copyright © 2018 The Things Network
# Use of this source code is governed by the
# MIT license that can be found in the LICENSE file.

from .application import ApplicationClient
from .ttnmqtt import MQTTClient
from .discovery import DiscoveryClient
from ttn.utils import stubs, read_key
import os

if os.getenv("GRPC_SSL_CIPHER_SUITES"):
    os.environ["GRPC_SSL_CIPHER_SUITES"] += os.pathsep + stubs.MODERN_CIPHER
else:
    os.environ["GRPC_SSL_CIPHER_SUITES"] = stubs.MODERN_CIPHER


class HandlerClient:

    def __init__(self, app_id,
                 app_access_key,
                 discovery_address="discovery.thethings.network:1900",
                 cert_path="",
                 insecure_channel=False):
        self.app_id = app_id
        self.app_access_key = app_access_key
        self.insecure_channel = insecure_channel
        if cert_path:
            cert = read_key(cert_path)
            self.__open(discovery_address, cert)
        else:
            self.__open(discovery_address)

    def __open(self, discovery_address, certificate=""):
        if not hasattr(self, 'announcement'):
            if certificate:
                discovery = DiscoveryClient(
                    discovery_address,
                    certificate,
                    insecure_channel=self.insecure_channel
                )
            else:
                discovery = DiscoveryClient(
                    discovery_address,
                    insecure_channel=self.insecure_channel
                )
            self.announcement = discovery.get_by_app_id(self.app_id)

    def data(self, reconnect=True):
        if not hasattr(self, "announcement"):
            raise RuntimeError("HandlerClient needs to be open before"
                               "it can create a data client.")

        return MQTTClient(self.app_id,
                          self.app_access_key,
                          mqtt_address=self.announcement.mqtt_address,
                          reconnect=reconnect)

    def application(self):
        if not hasattr(self, "announcement"):
            raise RuntimeError("HandlerClient needs to be open"
                               "before it can create a data client.")
        return ApplicationClient(self.app_id,
                                 self.app_access_key,
                                 handler_address=self.announcement.net_address,
                                 cert_content=self.announcement.certificate)
