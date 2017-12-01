import grpc
import github_com.TheThingsNetwork.api.handler.handler_pb2 as proto
import github_com.TheThingsNetwork.api.handler.handler_pb2_grpc as handler
import os
from utils import stubs

if os.getenv('GRPC_SSL_CIPHER_SUITES'):
    os.environ['GRPC_SSL_CIPHER_SUITES'] += os.pathsep + os.pathsep.join(
                                                stubs.MODERN_CIPHER_SUITES)
else:
    os.environ['GRPC_SSL_CIPHER_SUITES'] = stubs.MODERN_CIPHER_SUITES

credentials = grpc.ssl_channel_credentials(stubs.handler['certificate'])
channel = grpc.secure_channel(stubs.handlerAddress, credentials)
client = handler.ApplicationManagerStub(channel)

req = proto.ApplicationIdentifier()
req.app_id = stubs.apptest['appId']
meta = [('token', stubs.apptest['accessToken'])]
client.RegisterApplication(req, 1, meta)
