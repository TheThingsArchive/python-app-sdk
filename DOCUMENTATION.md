## Table of Contents
* [Description](#description)
* [MQTTClient](#mqttclient)
* [connect](#connect)
* [close](#close)
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

This package provides you an easy way to connect to The Things Network via MQTT.

### MQTTClient

The class constructor can be called following this scheme:
```python
mqtt(appID, appAccessKey, [mqttAddress])
```
- `appID`: **string**  this the name given to the application when it was created.
![Screenshot of the console with app section](./images/app-console.png?raw=true)
- `appAccessKey`: **string**  this can be found at the bottom of the application page under **ACCESS KEYS**.
![Screenshot of the console with accesskey section](./images/accesskey-console.png?raw=true)
- `mqttAddress`: **string**  this  is the address of the handler to which the application was registered.
The constructor returns an **MQTTClient object** set up with the application informations, connected to The Things Network.

### connect
This function connect your client, in case it was closed and need to be openned once again.
```python
client.connect()
```

### close
Disconnects the MQTT client from which we call the method..
```python
client.close()
```

### start
Starts an asynchronous loop for the client so that it's possible to run another process (such as a web server) in the same script. This loop is started by default when creating the MQTT client. So it should only be used in case the client was stopped and need to be started again, after re-connecting.
```python
client.start()
```

### stop
Stops the MQTT client and also disconnect it.
```python
client.stop()
```

### Using Callbacks

The callback functions are functions which are executed when a trigger event happens.

#### setUplinkCallback
Set the callback function, to be called when an uplink message is received.
```python
client.setUplinkCallback(uplinkCallback)
```

##### uplinkCallback
The callback function must be declared in your script following this structure:
* `uplinkCallback(msg, client)`
  * `msg`: **JSON object**  the message received by the client
  * `client`: **object**  the client from which the callback is executed are calling

#### setConnectCallback
Set the connection callback function to be executed when the client connect to the broker.
```python
client.setConnectCallback(connectCallback)
```
##### connectCallback
- `connectCallback(res, client)`: the function which will be executed on connection to the broker.
  - `res`: **boolean**  the result of the connection. If it's true, the connection succeeded went well. If not, it means the connection failed.
  - `client`: **object**  the TTN client from which the callback is called.

#### setDownlinkCallback
Set the downlink callback function, with actions to execute when a downlink message is sent.
```python
client.setDownlinkCallback(downlinkCallback)
```
##### downlinkCallback
- `downlinkCallback(mid, client)`: the function which will be the new publish behavior for our MQTT client.
  - `mid`: **int**  this is the message ID for the downlink request. It can be used to track the request.
  - `client`: **object**  the TTN client from which the callback is called.

#### setCloseCallback
Set the callback to be executed when the connection to the TTN broker is closed.
```python
client.setCloseCallback(closeCallback)
```
##### closeCallback
- `closeCallback(res, client)`: the function which will be executed when the connection is closed.
  - `res`: **boolean**  the result of the disconnection. If it's 0, it went well. If not, it means the disconnection was unexpected.
  - `client`: **object**  the TTN client from which we call the callback.

### send
Sends a downlink to the device.
```python
client.send(deviceID, payload, [port], [confirmation], [schedule])
```
- `deviceID`: **string**  the ID of the device you wish to send the message to.
- `payload`: the payload of the message to be published to the broker. It can be an hexadecimal **string**, a base64 **string** like `AQ==` (this will send the raw payload `01` to your device) or an object with several fields following the **JSON** standard. In case it's a **JSON** object with fields, please make sure the **encoder** function (Payload Formats section) of the application is set to make sense of the informations transmitted in each field.
![Screenshot of an encoder function in the console](./images/encoder-function.png?raw=true)
- `port`: **int**  the port of the device to which you wish to send the message. Default value to 1.
- `confirmation`: **boolean**  This boolean indicates if you wish to receive a confirmation after sending the downlink message. Default value to False.
- `schedule`: **string**  this string provide the type of schedule on which the message should be sent. It can take values such as `first` or `last`. Default value to `replace`.