import grpc
import github_com.TheThingsNetwork.api.handler.handler_pb2 as proto
import github_com.TheThingsNetwork.api.handler.handler_pb2_grpc as handler
import os
from utils import stubs

os.environ['GRPC_SSL_CIPHER_SUITES'] = "ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256"

credentials = grpc.ssl_channel_credentials(stubs.handler['certificate'])
channel = grpc.secure_channel(stubs.handlerAddress, credentials)
client = handler.ApplicationManagerStub(channel)

req = proto.ApplicationIdentifier()
req.app_id = stubs.apptest['appId']
meta = [('token', stubs.apptest['accessToken'])]
client.RegisterApplication(req, 1, meta)
