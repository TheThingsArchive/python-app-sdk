# The Things Network Python SDK

[![Build Status](https://travis-ci.org/TheThingsNetwork/python-app-sdk.svg?branch=master)](https://travis-ci.org/TheThingsNetwork/python-app-sdk)

![The Things Network](https://thethings.blob.core.windows.net/ttn/logo.svg)

This is the Python Application SDK for [The Things Network](https://www.thethingsnetwork.org/) to receive messages from IoT devices via The Things Network and sen messages as well.

## Installation
```
$ pip install ttnmqtt
```
## Documentation
* [API Reference](./DOCUMENTATION.md)

## Example
```python
import time
from ttnmqtt import MQTTClient as mqtt_client

app_id = "foo"
access_key = "ttn-account.eiPq8mEeYRL_PNBZsOpPy-O3ABJXYWulODmQGR5PZzg"

def uplink_callback(msg, client):
  print("Received uplink from ", msg.dev_id)
  print(msg)


my_client = mqtt_client(app_id, access_key)
my_client.set_uplink_callback(uplink_callback)
my_client.connect()
time.sleep(60)
my_client.close()
```

## License

Source code for The Things Network is released under the MIT License, which can be found in the [LICENSE](LICENSE) file. A list of authors can be found in the [AUTHORS](AUTHORS) file.
