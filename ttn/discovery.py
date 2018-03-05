# coding: Latin-1
# Copyright © 2018 The Things Network
# Use of this source code is governed by the
# MIT license that can be found in the LICENSE file.


import ttn.github_com.TheThingsNetwork.api.discovery.discovery_pb2_grpc \
    as disco
import ttn.github_com.TheThingsNetwork.api.discovery.discovery_pb2 as proto

import grpc
import os
from ttn.utils import stubs

if os.getenv("GRPC_SSL_CIPHER_SUITES"):
    os.environ["GRPC_SSL_CIPHER_SUITES"] += os.pathsep + stubs.MODERN_CIPHER
else:
    os.environ["GRPC_SSL_CIPHER_SUITES"] = stubs.MODERN_CIPHER


class DiscoveryClient:

    def __init__(self,
                 discovery_address="discovery.thethings.network:1900",
                 certificate=""):
        if certificate:
            creds = grpc.ssl_channel_credentials(certificate)
        else:
            creds = grpc.ssl_channel_credentials()
        channel = grpc.secure_channel(discovery_address, creds)
        self.client = disco.DiscoveryStub(channel)

    def get_all(self, service_name):
        req = proto.GetServiceRequest()
        req.service_name = service_name
        res = self.client.GetAll(req)
        return res.services

    def get(self, service_name, ID):
        req = proto.GetRequest()
        req.service_name = service_name
        req.id = ID
        return self.client.Get(req)

    def get_by_app_id(self, app_id):
        req = proto.GetByAppIDRequest()
        req.app_id = app_id
        return self.client.GetByAppID(req)
