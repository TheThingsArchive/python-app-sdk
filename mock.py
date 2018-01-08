import github_com.TheThingsNetwork.api.handler.handler_pb2 as proto
import github_com.TheThingsNetwork.api.protocol.lorawan.device_pb2 as lorawan
import github_com.TheThingsNetwork.api.handler.handler_pb2_grpc as handler

class MockApplicationManager:
    def __inti__(self):
        self.application = proto.Application()
        self.applicationIdentifier = proto.ApplicationIdentifier()
        self.device = proto.Device()
        self.deviceIdentifier = proto.DeviceIdentifier()
        self.deviceList = proto.DeviceList()
        self.err = None

    def reset(self):
        self.application = None
        self.applicationIdentifier = None
        self.device = None
        self.deviceIdentifier = None
        self.deviceList = None
        self.err = None

    def RegisterApplication(self, appid, timeout, meta):
        self.applicationIdentifier = appid
        return {"err": self.err}

    def GetApplication(self, req, timeout, meta):
        self.applicationIdentifier = req
        return {"application": self.application, "err": self.err}

    def SetApplication(self, app, timeout, meta):
        self.application = app
        return {"err": self.err}

    def DeleteApplication(self, appid, timeout, meta):
        self.applicationIdentifier = appid
        return {"err": self.err}

    def GetDevice(self, devid, timeout, meta):
        self.deviceIdentifier = devid
        return self.device

    def SetDevice(self, dev, timeout, meta):
        self.device = dev
        if self.deviceList == None:
            self.deviceList = proto.DeviceList()
        return {"err": self.err}

    def DeleteDevice(self, devid, timeout, meta):
        self.deviceIdentifier = devid
        self.device = None
        return {"err": self.err}

    def GetDevicesForApplication(self, appid, timeout, meta):
        self.applicationIdentifier = appid
        return self.deviceList
