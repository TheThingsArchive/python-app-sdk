import grpc, os, base64, json

import github_com.TheThingsNetwork.api.handler.handler_pb2 as proto
import github_com.TheThingsNetwork.api.protocol.lorawan.device_pb2 as lorawan
import github_com.TheThingsNetwork.api.handler.handler_pb2_grpc as handler

import github_com.TheThingsNetwork.api.discovery.discovery_pb2_grpc as discovery_pb2_grpc
import github_com.TheThingsNetwork.api.discovery.discovery_pb2 as discovery_pb2

from jose import jwt
from utils import is_token, read_key, stubs

os.environ['GRPC_SSL_CIPHER_SUITES'] = stubs.MODERN_CIPHER_SUITES

class ApplicationClient:

    def __init__(self, app_id, token_or_key, net_address=None, certificate=None):
        self.app_id = app_id
        self.net_address = net_address
        self.credentials = certificate

        if is_token(token_or_key):
            self.app_access_token = token_or_key
        else:
            self.app_access_key = token_or_key

        if self.net_address is None:
            discocreds = grpc.ssl_channel_credentials()
            channel = grpc.secure_channel('discovery.thethings.network:1900', discocreds)
            discoStub = discovery_pb2_grpc.DiscoveryStub(channel)
            req = discovery_pb2.GetByAppIDRequest()
            req.app_id = self.app_id
            announcement = discoStub.GetByAppID(req)
            self.net_address = announcement.net_address
            self.credentials = announcement.certificate
        elif self.credentials is None:
            raise ValueError("You need to provide credentials")

        creds = grpc.ssl_channel_credentials(self.credentials)
        channel = grpc.secure_channel(self.net_address, creds)
        self.client = handler.ApplicationManagerStub(channel)

    def __create_metadata(self):
        if hasattr(self, 'app_access_token'):
            return [('token', self.app_access_token)]
        elif hasattr(self, 'app_access_key'):
            return [('key', self.app_access_key)]

    def get(self):
        req = proto.ApplicationIdentifier()
        req.app_id = self.app_id
        meta = self.__create_metadata()
        try:
            app = self.client.GetApplication(req, 60, meta)
            return app
        except grpc.RpcError as err:
            raise RuntimeError("Error while getting the application: {}".format(err.code().name))

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

    def set_register_on_join_access_key(self, to):
        self.__set({
            "register_on_join_access_key": to,
        })

    def unregister(self):
        req = proto.ApplicationIdentifier()
        req.app_id = self.app_id
        meta = self.__create_metadata()
        return self.client.DeleteApplication(req, 60, meta)

    def __set(self, updates):
        req = proto.Application()
        req.app_id = self.app_id

        if "payload_format" in updates:
          req.payload_format = updates['payload_format']

        if "register_on_join_access_key" in updates:
          req.register_on_join_access_key = updates['register_on_join_access_key']

        if "decoder" in updates:
          req.decoder = updates['decoder']

        if "converter" in updates:
          req.converter = updates['converter']

        if "encoder" in updates:
          req.encoder = updates['encoder']

        if "validator" in updates:
          req.validator = updates['validator']

        meta = self.__create_metadata()
        return self.client.SetApplication(req, 60, meta)

    def register_device(self, devID, device):
        return self.__setDevice(devID, device)

    def __setDevice(self, devID, device):
        req = self.__deviceRequest(devID, device)
        meta = self.__create_metadata()
        return self.client.SetDevice(req, 60, meta)

    def devices(self):
        req = proto.ApplicationIdentifier()
        req.app_id = self.app_id
        meta = self.__create_metadata()
        res = self.client.GetDevicesForApplication(req, 60, meta)
        return res.devices

    def device(self, devID):
        req = proto.DeviceIdentifier()
        req.app_id = self.app_id
        req.dev_id = devID
        meta = self.__create_metadata()
        res = self.client.GetDevice(req, 60, meta)
        return res

    def update_device(self, dev_id, updates):
        device = self.device(dev_id)
        req = self.__deviceRequest(dev_id, updates, True)
        meta = self.__create_metadata()
        return self.client.SetDevice(req, 60, meta)

    def delete_device(self, dev_id):
        req = proto.DeviceIdentifier()
        req.app_id = self.app_id
        req.dev_id = dev_id
        meta = self.__create_metadata()
        return self.client.DeleteDevice(req, 60, meta)

    def __deviceRequest(self, dev_id, device, update=False):
        if update:
            req = self.device(dev_id)
            req.lorawan_device.CopyFrom(self.__lorawanDeviceRequest(dev_id, device, True))
        else:
            req = proto.Device()
            req.lorawan_device.CopyFrom(self.__lorawanDeviceRequest(dev_id, device))
        req.app_id = self.app_id
        req.dev_id = dev_id

        if "description" in device:
          req.description = device['description']

        if "latitude" in device:
          req.latitude = device['latitude']

        if "longitude" in device:
          req.longitude = device['longitude']

        if "altitude" in device:
          req.altitude = device['altitude']

        if "attributes" in device:
            for k, v in device['attributes'].items():
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
