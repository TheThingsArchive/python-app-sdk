# coding: Latin-1
# Copyright © 2018 The Things Network
# Use of this source code is governed by the
# MIT license that can be found in the LICENSE file.


import grpc
import os
import base64


import ttn.github_com.TheThingsNetwork.api.handler.handler_pb2 as proto
import ttn.github_com.TheThingsNetwork.api.protocol.lorawan.device_pb2 \
    as lorawan
import ttn.github_com.TheThingsNetwork.api.handler.handler_pb2_grpc as handler
from ttn.utils import stubs

from .discovery import DiscoveryClient


if os.getenv("GRPC_SSL_CIPHER_SUITES"):
    os.environ["GRPC_SSL_CIPHER_SUITES"] += os.pathsep + stubs.MODERN_CIPHER
else:
    os.environ["GRPC_SSL_CIPHER_SUITES"] = stubs.MODERN_CIPHER


# time out in seconds
TIME_OUT = 30


class ApplicationClient:

    def __init__(self, app_id, access_key,
                 net_address="", cert_content="",
                 discovery_address="discovery.thethings.network:1900"):
        self.app_id = app_id
        self.app_access_key = access_key

        if not net_address:
            discovery = DiscoveryClient(discovery_address)
            announcement = discovery.get_by_app_id(self.app_id.encode())
            net_address = announcement.net_address
            cert_content = announcement.certificate
        elif not cert_content:
            raise RuntimeError("You need to provide credentials")

        creds = grpc.ssl_channel_credentials(cert_content.encode())
        channel = grpc.secure_channel(net_address, creds)
        self.client = handler.ApplicationManagerStub(channel)

    def __create_metadata(self):
        return [("key", self.app_access_key)]

    def get(self):
        req = proto.ApplicationIdentifier()
        req.app_id = self.app_id.encode()
        meta = self.__create_metadata()
        try:
            app = self.client.GetApplication(req, TIME_OUT, meta)
            return app
        except grpc.RpcError as err:
            raise RuntimeError(
                "Error while getting the",
                " application: {}".format(err.code().name))

    def set_payload_format(self, payloadf):
        self.__set({
          "payload_format": payloadf,
        })

    def set_custom_payload_functions(self, **kwargs):
        updates = {
            "payload_format": "custom",
        }
        for k, v in kwargs.items():
            print(k, v)
            updates[k] = v
        self.__set(updates)

    def unregister(self):
        req = proto.ApplicationIdentifier()
        req.app_id = self.app_id
        meta = self.__create_metadata()
        try:
            return self.client.DeleteApplication(req, TIME_OUT, meta)
        except grpc.RpcError as err:
            raise RuntimeError(
                "Error while deleting the",
                " application: {}".format(err.code().name))

    def __set(self, updates):
        req = proto.Application()
        req.app_id = self.app_id

        if "payload_format" in updates:
            req.payload_format = updates["payload_format"]

        if "register_on_join_access_key" in updates:
            req.register_on_join_access_key = updates[("register_on_"
                                                       "join_access_key")]

        if "decoder" in updates:
            req.decoder = updates["decoder"]

        if "converter" in updates:
            req.converter = updates["converter"]

        if "encoder" in updates:
            req.encoder = updates["encoder"]

        if "validator" in updates:
            req.validator = updates["validator"]

        meta = self.__create_metadata()
        try:
            return self.client.SetApplication(req, TIME_OUT, meta)
        except grpc.RpcError as err:
            raise RuntimeError(
                "Error while updating the",
                " application: {}".format(err.code().name))

    def register_device(self, devID, device):
        return self.__setDevice(devID, device)

    def __setDevice(self, devID, device):
        req = self.__deviceRequest(devID, device)
        meta = self.__create_metadata()
        try:
            return self.client.SetDevice(req, TIME_OUT, meta)
        except grpc.RpcError as err:
            raise RuntimeError(
                "Error when updating the",
                " device: {}".format(err.code().name))

    def devices(self):
        req = proto.ApplicationIdentifier()
        req.app_id = self.app_id
        meta = self.__create_metadata()
        try:
            res = self.client.GetDevicesForApplication(req, TIME_OUT, meta)
            return res.devices
        except grpc.RpcError as err:
            raise RuntimeError(
                "Error while getting the",
                " list of devices: {}".format(err.code().name))

    def device(self, devID):
        req = proto.DeviceIdentifier()
        req.app_id = self.app_id
        req.dev_id = devID
        meta = self.__create_metadata()
        try:
            res = self.client.GetDevice(req, TIME_OUT, meta)
            return res
        except grpc.RpcError as err:
            raise RuntimeError(
                "Error while getting the",
                " device: {}".format(err.code().name))

    def update_device(self, dev_id, updates):
        device = self.device(dev_id)
        req = self.__deviceRequest(dev_id, updates, True)
        meta = self.__create_metadata()
        try:
            return self.client.SetDevice(req, TIME_OUT, meta)
        except grpc.RpcError as err:
            raise RuntimeError(
                "Error while updating the",
                " device: {}".format(err.code().name))

    def delete_device(self, dev_id):
        req = proto.DeviceIdentifier()
        req.app_id = self.app_id
        req.dev_id = dev_id
        meta = self.__create_metadata()
        try:
            return self.client.DeleteDevice(req, 60, meta)
        except grpc.RpcError as err:
            raise RuntimeError(
                "Error while deleting the",
                " device: {}".format(err.code().name))

    def __deviceRequest(self, dev_id, device, update=False):
        if update:
            req = self.device(dev_id)
            req.lorawan_device.CopyFrom(self.__lorawanDeviceRequest(dev_id,
                                                                    device,
                                                                    True))
        else:
            req = proto.Device()
            req.lorawan_device.CopyFrom(self.__lorawanDeviceRequest(dev_id,
                                                                    device))
        req.app_id = self.app_id
        req.dev_id = dev_id

        if "description" in device:
            req.description = device["description"]

        if "latitude" in device:
            req.latitude = device["latitude"]

        if "longitude" in device:
            req.longitude = device["longitude"]

        if "altitude" in device:
            req.altitude = device["altitude"]

        if "attributes" in device:
            for k, v in device["attributes"].items():
                req.attributes[k] = v

        return req

    def __lorawanDeviceRequest(self, dev_id, device, update=False):
        if update:
            req = self.device(dev_id).lorawan_device
        else:
            req = lorawan.Device()
        req.app_id = self.app_id
        req.dev_id = dev_id

        if "appEui" in device:
            req.app_eui = base64.b16decode(device["appEui"])

        if "devEui" in device:
            req.dev_eui = base64.b16decode(device["devEui"])

        if "devAddr" in device:
            req.dev_addr = base64.b16decode(device["devAddr"])

        if "nwkSKey" in device:
            req.nwk_s_key = base64.b16decode(device["nwkSKey"])

        if "appSKey" in device:
            req.app_s_key = base64.b16decode(device["appSKey"])

        if "appKey" in device:
            req.app_key = base64.b16decode(device["appKey"])

        if "fCntUp" in device:
            req.f_cnt_up = device["fCntUp"]

        if "fCntDown" in device:
            req.f_cnt_down = device["fCntDown"]

        if "disableFCntCheck" in device:
            req.disable_f_cnt_check = device["disableFCntCheck"]

        if "uses32BitFCnt" in device:
            req.uses32_bit_f_cnt = device["uses32BitFCnt"]

        return req
