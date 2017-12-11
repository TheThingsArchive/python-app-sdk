import ttn
import time
from utils import stubs

def test_handler():
    handler = ttn.HandlerClient("test-python-sdk",
                                  ("ttn-account-v2.suDG-8zvpIFL42r-f6qRcMj"
                                   "_Na5O2Dm_IH8Up6BcrAY"))
    appclient = handler.application()
    mqttclient = handler.data()
    assert isinstance(appclient, ttn.ApplicationClient) and isinstance(mqttclient, ttn.MQTTClient)
