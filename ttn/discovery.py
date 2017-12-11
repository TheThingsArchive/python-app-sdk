# coding: Latin-1
# Copyright © 2017 The Things Network
# Use of this source code is governed by the
# MIT license that can be found in the LICENSE file.


import github_com.TheThingsNetwork.api.discovery.discovery_pb2_grpc as disco
import github_com.TheThingsNetwork.api.discovery.discovery_pb2 as proto

import grpc
import os
from utils import stubs

os.environ["GRPC_SSL_CIPHER_SUITES"] = stubs.MODERN_CIPHER_SUITES


class DiscoveryClient:

    def __init__(self, discovery_address=None, certificate=None):
        if discovery_address is None:
            self.discovery_address = "discovery.thethings.network:1900"

        if not certificate is None:
            self.certificate = certificate


    def get_by_app_id(self, app_id):
        req = proto.GetByAppIDRequest()
        req.app_id = app_id
        if hasattr(self, "certificate"):
            creds = grpc.ssl_channel_credentials(self.certificate)
        else:
            creds = grpc.ssl_channel_credentials()
        channel = grpc.secure_channel(self.discovery_address, creds)
        stub = disco.DiscoveryStub(channel)
        return stub.GetByAppID(req)
