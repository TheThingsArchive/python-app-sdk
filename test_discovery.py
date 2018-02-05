# coding: Latin-1
# Copyright © 2018 The Things Network
# Use of this source code is governed by the
# MIT license that can be found in the LICENSE file.

import unittest
from ttn import DiscoveryClient
from utils import stubs

class TestDiscoveryClient(unittest.TestCase):

    def setUp(self):
        self.discovery = DiscoveryClient()

    def test_constructor_discovery(self):
        assert hasattr(self.discovery, "client")


    def test_get_by_app_id(self):
        res = self.discovery.get_by_app_id("test-python-sdk")
        assert res.id == "ttn-handler-eu"


    def test_get(self):
        res = self.discovery.get("handler", "ttn-handler-eu")
        assert res


    def test_get_all(self):
        res = self.discovery.get_all("handler")
        assert res
