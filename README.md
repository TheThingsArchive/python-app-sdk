# The Things Network Python SDK

[![Build Status](https://travis-ci.org/TheThingsNetwork/python-app-sdk.svg?branch=master)](https://travis-ci.org/TheThingsNetwork/python-app-sdk)

![The Things Network](https://thethings.blob.core.windows.net/ttn/logo.svg)

## Table of Contents
* [Description](#description)
* [MQTTClient](#mqttclient)
* [connect](#connect)
* [close](#close)
* [startForever](#startforever)
* [start](#start)
* [stop](#stop)
* [setUplinkCallback](#setuplinkcallback)
  * [uplinkCallback](#uplinkcallback)
* [setConnectCallback](#setconnectcallback)
  * [connectCallback](#connectcallback)
* [setDownlinkCallback](#setpublishcallback)
  * [downlinkCallback](#publishcallback)
* [setCloseCallback](#setclosecallback)
  * [closeCallback](#closecallback)
* [send](#send)
* [License](#license)

## Description

This package provides you an easy way to connect to The Things Network via MQTT. Take note that, you'll first need to create an application with a device to run the constructor of the MQTT client because you need to provide, an applicationID and a deviceID.
First include the package in your file like this:
```python
from ttnmqtt import MQTTClient as mqtt
```

### MQTTClient

The class constructor can be called following this scheme:
```python
mqtt(appID, appAccessKey, [mqttAddress])
```
- `appID`: *string*, this the name you gave your application when you created it.
- `appAccessKey`: *string*, it can be found at the bottom of your application page under **ACCESS KEYS**.
- `mqttAddress`: *string*, this the address of the handler to which your application was registered. If you registered to a personnal or private handler, please provide the address, if not you don't need to provide this argument. Please make sure you also give the port number when providing the mqttAddress.
All the above informations can be found in your The Things Network console.
The constructor returns an *MQTTClient object* set up with your application informations, ready for connection.

### connect
This function connect your client, in case you closed it and which to open the connection once again.
```python
client.connect()
```

### close
Disconnects the MQTT client from which we call the method. Also able to stop a forever loop in case the client was running on a loop launched by the `startForever()` method.
```python
client.close()
```

### startForever
A background loop is started by default when creating an MQTT client but in in case you wish to start a loop as the main loop of your process. You can start a forever loop with this method. You wont be able to run anything else at the same time on this script.
```python
client.startForever()
```

### start
Starts a loop for the client in the background so that it's possible to run another process (such as a web server) in the same script. This loop is started by default when creating the MQTT client. So it should only be used in case the client was stopped and you wish to start it again after re-connecting.
```python
client.start()
```

### stop
Stops the MQTT client and also disconnect it.
```python
client.stop()
```

### Using Callbacks

The callback functions are functions which are executed when a trigger event happens. They should be set right after the MQTT client creation so that they don't miss any event.

#### setUplinkCallback
Set the callback function, to be called when an uplink message is received.
```python
client.setUplinkCallback(uplinkCallback)
```

##### uplinkCallback
The callback function must be declared in your script following this structure:
* `uplinkCallback(msg, client)`
  * `msg`: *JSON object*, the message received by the client
  * `client`: *object*, the client from which the callback is executed are calling

On each message reception, you should see **receving message from** in the console, and the callback will be executed.

#### setConnectCallback
Set the connection callback function to be executed when the client connect to the broker.
```python
client.setConnectCallback(connectCallback)
```
##### connectCallback
- `connectCallback(res, client)`: the function which will be executed on connection to the broker.
  - `res`: *int*, the result of the connection. If it's 0, it went well. If not, it means the connection failed.
  - `client`: *object*, the TTN client from which we call the callback.

#### setDownlinkCallback
Set the downlink callback function, with actions to execute when a downlink message is sent.
```python
client.setDownlinkCallback(downlinkCallback)
```
##### downlinkCallback
- `downlinkCallback(mid, client)`: the function which will be the new publish behavior for our MQTT client.
  - `mid`: *int*, it matches the mid variable returned from the publish call to allow sent messages to be tracked.
  - `client`: *object*, the TTN client from which we call the callback.

#### setCloseCallback
Set the callback to be executed when the connection to the TTN broker is closed.
```python
client.setCloseCallback(closeCallback)
```
##### closeCallback
- `closeCallback(res, client)`: the function which will be executed when the connection is closed.
  - `res`: *int*, the result of the disconnection. If it's 0, it went well. If not, it means the disconnection was unexpected.
  - `client`: *object*, the TTN client from which we call the callback.

### send
Publishes a message to the MQTT broker.
```python
client.send(deviceID, payload, [port], [confirmation], [schedule])
```
- `deviceID`: *string*, the ID of the device you wish to send the message to.
- `payload`: the payload of the message to be published to the broker. It can be an hexadecimal *string* like `AQ==` (this will send the raw payload `00` to your device) or an object with several fields following the *JSON* standard.
- `port`: *int*, the port of the device to which you wish to send the message. Default value to 1.
- `confirmation`: *boolean*, this boolean indicates if you wish to receive a confirmation after sending the downlink message. Default value to False.
- `schedule`: *string*, this string provide the type of schedule on which the message should be sent it can take values such as `first` or `last`. Default value to `replace`.

## License

Source code for The Things Network is released under the MIT License, which can be found in the [LICENSE](LICENSE) file. A list of authors can be found in the [AUTHORS](AUTHORS) file.
