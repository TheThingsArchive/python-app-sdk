# coding: Latin-1
# Copyright © 2017 The Things Network
# Use of this source code is governed by the
# MIT license that can be found in the LICENSE file.


import unittest
import ttn
import time
from utils import stubs

class TestHandlerClient(unittest.TestCase):

    def setUp(self):
        self.handler = ttn.HandlerClient("test-python-sdk",
                                    ("ttn-account-v2.suDG-8zvpIFL42r-f6qRcMj"
                                     "_Na5O2Dm_IH8Up6BcrAY"))

    def test_handler(self):
        self.appclient = self.handler.application()
        self.mqttclient = self.handler.data()
        assert isinstance(self.appclient,
                          ttn.ApplicationClient) and \
            isinstance(self.mqttclient, ttn.MQTTClient)
