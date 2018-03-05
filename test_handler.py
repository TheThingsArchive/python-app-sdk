# coding: Latin-1
# Copyright © 2018 The Things Network
# Use of this source code is governed by the
# MIT license that can be found in the LICENSE file.


import unittest
import ttn
from ttn.utils import stubs

class TestHandlerClient(unittest.TestCase):

    def setUp(self):
        self.handler = ttn.HandlerClient(stubs.apptest["appId"],
                                         stubs.apptest["accessKey"])

    def test_handler(self):
        self.appclient = self.handler.application()
        self.mqttclient = self.handler.data()
        assert isinstance(self.appclient,
                          ttn.ApplicationClient) and \
            isinstance(self.mqttclient, ttn.MQTTClient)
