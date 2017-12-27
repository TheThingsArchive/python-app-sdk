# The Things Network Python SDK

[![Build Status](https://travis-ci.org/TheThingsNetwork/python-app-sdk.svg?branch=master)](https://travis-ci.org/TheThingsNetwork/python-app-sdk)

![The Things Network](https://thethings.blob.core.windows.net/ttn/logo.svg)

This is the Python Application SDK for [The Things Network](https://www.thethingsnetwork.org/) to receive messages from IoT devices via The Things Network and send messages as well.

## Installation
```
$ pip install ttn
```
## Documentation
* [API Reference](./DOCUMENTATION.md)

## Example
```python
import time
import ttn

app_id = "foo"
access_key = "ttn-account.eiPq8mEeYRL_PNBZsOpPy-O3ABJXYWulODmQGR5PZzg"

# using mqtt client
def uplink_callback(msg, client):
  print("Received uplink from ", msg.dev_id)
  print(msg)

mqtt_client = ttn.MQTTClient(app_id, access_key)
mqtt_client.set_uplink_callback(uplink_callback)
mqtt_client.connect()
time.sleep(60)
mqtt_client.close()

# using application manager client
app_client =  ttn.ApplicationClient(app_id, access_key)
my_app = app_client.get()
print(my_app)
my_devices = app_client.devices()
print(my_devices)
```

## License

Source code for The Things Network is released under the MIT License, which can be found in the [LICENSE](LICENSE) file. A list of authors can be found in the [AUTHORS](AUTHORS) file.
