# coding: Latin-1
# Copyright © 2018 The Things Network
# Use of this source code is governed by the
# MIT license that can be found in the LICENSE file.


import unittest
from mock import MockApplicationManager
from ttn import ApplicationClient
import github_com.TheThingsNetwork.api.handler.handler_pb2 as handler
import github_com.TheThingsNetwork.api.protocol.lorawan.device_pb2 as lorawan
from utils import stubs
import binascii


class TestApplicationClient(unittest.TestCase):

    def setUp(self):
        self.mock = MockApplicationManager()
        self.manager = ApplicationClient("test", "pswd")
        self.manager.client = self.mock

    def test_get(self):
        self.mock.reset()
        self.mock.application = handler.Application()
        self.mock.application.app_id = "test"
        res = self.manager.get()
        assert res["application"].app_id == "test"

    def test_payload_format(self):
        self.mock.reset()
        self.mock.application = handler.Application()
        self.mock.application.payload_format = "custom"
        res = self.manager.get()
        assert res["application"].payload_format == "custom"

        self.manager.set_payload_format("other")
        assert self.mock.application.payload_format == "other"

    def test_custom_payload(self):
        self.mock.reset()
        self.mock.application = handler.Application()
        self.mock.application.payload_format = "custom"
        self.mock.application.decoder = "decoder"
        self.mock.application.converter = "converter"
        self.mock.application.validator ="validator"
        self.mock.application.encoder = "encoder"
        res = self.manager.get()
        assert res["application"].payload_format == "custom" and \
            res["application"].validator =="validator" and \
                res["application"].decoder =="decoder"

        self.manager.set_custom_payload_functions(validator="nvalidator",
                                                        decoder="ndecoder")
        res = self.manager.get()
        assert res["application"].payload_format == "custom" and \
            res["application"].validator =="nvalidator" and \
                res["application"].decoder =="ndecoder"

    def test_device(self):
        self.mock.reset()
        self.manager.register_device("foo", stubs.devicetest)
        res = self.manager.device("foo")
        assert res.dev_id == "foo"

        res = self.manager.devices()
        assert res is not None

        update = {
            "devEui": "1100223344556677",
        }
        self.manager.update_device("foo", update)
        res = self.manager.device("foo")
        assert res.lorawan_device.dev_eui == binascii.unhexlify("110022"
                                                                "3344556677")

        self.manager.delete_device("foo")
        res = self.manager.device("foo")
        assert res is None
