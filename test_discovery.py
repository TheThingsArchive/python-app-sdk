# coding: Latin-1
# Copyright © 2018 The Things Network
# Use of this source code is governed by the
# MIT license that can be found in the LICENSE file.

import unittest
from mock import patch

from ttn import DiscoveryClient


class TestDiscoveryClient(unittest.TestCase):

    def test_constructor_discovery(self):
        self.discovery = DiscoveryClient()
        assert hasattr(self.discovery, "client")

    @patch("grpc.secure_channel")
    def test_default_insecure_channel_set_to_false(self, mock_grpc_secure_channel):
        self.discovery = DiscoveryClient()
        assert mock_grpc_secure_channel.call_count == 1

    @patch("grpc.insecure_channel")
    def test_insecure_channel_called(self,mock_grpc_insecure_channel):
        self.discovery = DiscoveryClient(insecure_channel=True)
        assert mock_grpc_insecure_channel.call_count == 1

    def test_get_by_app_id(self):
        self.discovery = DiscoveryClient()
        res = self.discovery.get_by_app_id("test-python-sdk")
        assert res.id == "ttn-handler-eu"


    def test_get(self):
        self.discovery = DiscoveryClient()
        res = self.discovery.get("handler", "ttn-handler-eu")
        assert res


    def test_get_all(self):
        self.discovery = DiscoveryClient()
        res = self.discovery.get_all("handler")
        assert res
