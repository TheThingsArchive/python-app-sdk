# Table of Contents
* [Description](#description)
* [MQTTClient](#mqttclient)
  * [connect](#connect)
  * [close](#close)
  * [set_uplink_callback](#set_uplink_callback)
    * [uplink_callback](#uplink_callback)
  * [set_connect_callback](#set_connect_callback)
    * [connect_callback](#connect_callback)
  * [set_downlink_callback](#set_downlink_callback)
    * [downlink_callback](#downlink_callback)
  * [set_close_callback](#set_close_callback)
    * [close_callback](#close_callback)
  * [send](#send)
  * [UplinkMessage](#uplinkmessage)
* [ApplicationClient](#applicationclient)
  * [get](#get)
  * [set_payload_format](#set_payload_format)
  * [set_custom_payload_functions](#set_custom_payload_functions)
  * [set_register_on_join_access_key](#set_register_on_join_access_key)
  * [unregister](#unregister)
  * [device](#device)
  * [devices](#devices)
  * [update_device](#update_device)
  * [delete_device](#delete_device)
  * [Device](#device)
  * [Application](#application)
* [HandlerClient](#handlerclient)
  * [data](#data)
  * [application](#application)
* [Errors](#errors)


## Description
This package provides you an easy way to connect to The Things Network via MQTT or manage your applications.


## MQTTClient
The class constructor can be called following this scheme:
```python
MQTTClient(app_id, app_access_key, [mqtt_address], [discovery_address])
```
- `app_id`: **string**  this the name given to the application when it was created.
![Screenshot of the console with app section](./images/app-console.png?raw=true)
- `app_access_key`: **string**  this can be found at the bottom of the application page under **ACCESS KEYS**.
![Screenshot of the console with accesskey section](./images/accesskey-console.png?raw=true)
- `mqtt_address`: **string**  this  is the address of the handler to which the application was registered. It needs to be provided as an `mqtt_address=value` argument when calling the constructor.
- `discovery_address`: **string**  this is the address of the discovery server to use in order to find back the address of the MQTT handler. It needs to be provided as an `discovery_address=value` argument when calling the constructor.
The constructor returns an **MQTTClient object** set up with the application informations, ready to be connected to The Things Network.

### connect
Connects and starts the client in the background. This function also re-establishes the client's connection in case it was closed.
```python
client.connect()
```

### close
Disconnects and stops the client from which the method is called.
```python
client.close()
```

### Using Callbacks

The callback functions are functions which are executed when a trigger event happens.

#### set_uplink_callback
Add a callback function, to be called when an uplink message is received.
```python
client.set_uplink_callback(uplink_callback)
```

##### uplink_callback
The callback function must be declared in the script following this structure:
* `uplink_callback(msg, client)`
  * `msg`: **UplinkMessage object**  the message received by the client.
  * `client`: **MQTTClient object**  the client from which the callback is executed.

#### set_connect_callback
Add a connection callback function to be executed when the client connects to the broker.
```python
client.set_connect_callback(connect_callback)
```
##### connect_callback
- `connect_callback(res, client)`: the function which will be executed on connection to the broker.
  - `res`: **boolean**  the result of the connection. If it's true, the connection succeeded. If not, it means the connection failed.
  - `client`: **MQTTClient object**  the TTN client from which the callback is called.

#### set_downlink_callback
Add a downlink callback function, with actions to execute when a downlink message is sent.
```python
client.set_downlink_callback(downlinkCallback)
```
##### downlink_callback
- `downlink_callback(mid, client)`: the function which will be a new publish behavior for our MQTT client.
  - `mid`: **int**  this is the message ID for the downlink request. It can be used to track the request.
  - `client`: **MQTTClient object**  the TTN client from which the callback is called.

#### set_close_callback
Add a callback to be executed when the connection to the TTN broker is closed.
```python
client.set_close_callback(close_callback)
```
##### close_callback
- `close_callback(res, client)`: the function which will be executed when the connection is closed.
  - `res`: **boolean**  the result of the disconnection. If it's true, it went all as expected. If not, it means the disconnection was unexpected.
  - `client`: **MQTTClient object**  the TTN client from which we call the callback.

### send
Sends a downlink to the device.
```python
client.send(dev_id, payload, [port], [confirmation], [schedule])
```
- `dev_id`: **string**  the ID of the device which will receive the message.
- `payload`: the payload of the message to be published to the broker. It can be an hexadecimal **string**, a base64 **string** like `AQ==` (this will send the raw payload `01` to your device) or a **dictionary** of JSON nature. Here is an example of a **dictionary** argument that could be passed to the method:
```json
{"led_state": "on", "counter": 1}
```
In case it's a **dictionary** with fields, please make sure the **encoder** function (Payload Formats section) of the application is set to make sense of the informations transmitted in each field.
![Screenshot of an encoder function in the console](./images/encoder-function.png?raw=true)
- `port`: **int**  the port of the device to which the message will be sent. Default value to 1.
- `confirmation`: **boolean**  this boolean indicates if you wish to receive a confirmation after sending the downlink message. Default value to False.
- `schedule`: **string**  this string provides the type of schedule on which the message should be sent. It can take values such as `first` or `last`. Default value to `replace`.

### UplinkMessage
This type of object is constructed dynamically from the message received by the client, so this means some attributes can change from one message to another. However here are some constant attributes usually found in UplinkMessage objects:
* `app_id`: the application ID to which the device is registered
* `dev_id`: the ID of the device
* `port`: the port number on which the message was sent
* `payload_raw`: a buffer which contains the payload in hexadecimal
* `metadata`: this field is another object which contains all the metadata of the message. Such as: the date, the frequency, the data rate and the list of gateways.


## ApplicationClient
The class constructor can be called following this scheme:
```python
ApplicationClient(app_id, access_key_or_token, [net_address], [certificate], [discovery_address])
```
- `app_id`: **string**  this the name given to the application when it was created.
![Screenshot of the console with app section](./images/app-console.png?raw=true)
- `access_key_or_token`: **string**  this can be found at the bottom of the application page under **ACCESS KEYS**. You will need a key allowing you to change the settings if you wish to update your application.
- `net_address`: **string**  this  is the address of the handler to which the application was registered. It needs to be provided as a `net_address=value` argument when calling the constructor.
- `certificate`: **string**  this is the content of the certificate used to connect in a secure way to the handler. It needs to be provided as a `certificate=value` argument when calling the constructor.
- `discovery_address`: **string**  this is the address of the discovery server to use in order to find back the address of the handler to which the application in registered. It needs to be provided as a `discovery_address=value` argument when calling the constructor.
The constructor returns an **ApplicationClient** object set up with the application informations, ready to get the application registered on The Things Network.

### get
Gives back the [**Application**](#application) object with the id given to the constructor.
```python
client.get()
```

### set_payload_format
Sets the payload format of the application.
```python
client.set_payload_format(payload_format)
```
- payload_format: **string**  the new payload format.

### set_custom_payload_functions
Sets the payload functions of the application.
```python
client.set_custom_payload_functions([decoder], [encoder], [validator], [converter])
```
- `decoder`: **string**  decoder function that must be written in javascript, it needs to be provided as a `decoder=value` argument when calling the method.
- `encoder`: **string**  encoder function that must be written in javascript, it needs to be provided as a `encoder=value` argument when calling the method.
- `validator`: **string**  validator function that must be written in javascript, it needs to be provided as a `validator=value` argument when calling the method.
- `converter`: **string**  converter function that must be written in javascript, it needs to be provided as a `converter=value` argument when calling the method.

### set_register_on_join_access_key
Sets the register on join access key of the application.
```python
client.set_register_on_join_access_key(register_on_join)
```
- `register_on_join`: **string**  the `register_on_join` access key.

### unregister
Unregisters the application of the id provided to the constructor on creation of the client.
```python
client.unregister()
```

### register_device
Registers a new device to the application.
```python
client.register_device(dev_id, device)
```
- `dev_id`: **string**  the id of the device to be registered.
- `device`: **dictionary**  the dictionary with fields to be set as a new device of the application. See the [Device](#device) section to know the structure of the dictionary that should be passed and the name of the fields.

### device
Gives back the [**Device**](#device) object of the given id.
```python
client.device(dev_id)
```
- `dev_id`: **string**  the id of the device which is given back by the method.

### devices
Gives back the list of all the devices registered to the application.
```python
client.devices()
```

### update_device
Updates an already existing device of the application.
```python
client.update_device(dev_id, updates)
```
- `dev_id`: **string**  the id of the device to be updated.
- `updates`: **dictionary**  a dictionary with the fields to be updated in the device.

### delete_device
Deletes the device with the given id.
```python
client.delete_device(dev_id)
```
- `dev_id`: **string**  the id of the device to be deleted.

### Device
This objet is returned by the method `device()` of the ApplicationClient class. Here are its attributes:
* `app_id`: **string**
* `dev_id`: **string**
* `latitude`: **float**
* `longitude`: **float**
* `altitude`: **float**
* `description`: **string**
* `attributes`: **dictionary**
* `lorawan_device`: **dictionary**
    * `app_eui`: **string**  8 bytes in hexadecimal
    * `dev_eui`: **string**  8 bytes in hexadecimal
    * `dev_addr`: **string**  4 bytes in hexadecimal
    * `nwk_s_key`: **string**  16 bytes in hexadecimal
    * `app_s_key`: **string**  16 bytes in hexadecimal
    * `app_key`: **string**  16 bytes in hexadecimal
    * `f_cnt_up`: **int**
    * `f_cnt_down`: **int**
    * `disable_f_cnt_check`: **boolean**
    * `uses32_bit_f_cnt`: **boolean**

### Application
This object is returned by the method `get()` of the ApplicationClient class. Here are its attributes:
* `app_id`: **string**
* `payload_format`: **string**
* `decoder`: **string**
* `encoder`: **string**
* `converter`: **string**
* `validator`: **string**
* `register_on_join_access_key`: **string**

## HandlerClient
The class constructor can be called following this scheme:
```python
HandlerClient(app_id, access_key_or_token, [discovery_address], [certificate])
```
- `app_id`: **string**  this the name given to the application when it was created.
![Screenshot of the console with app section](./images/app-console.png?raw=true)
- `app_access_key`: **string**  this can be found at the bottom of the application page under **ACCESS KEYS**. You will need a key allowing you to change the settings if you wish to update your application.
- `discovery_address`: **string**  this is the address of the discovery server to use in order to find back the address of the handler to which the application in registered. Default to `None`.
- `certificate`: **string**  this is the certificate used to connect in a secure way to the discovery server. Default to `None`.

### data
Opens an MQTT client that can be used to receive uplink from devices registered to an application or send downlink to those same devices.
```python
handler.data()
```
Returns an [**MQTTClient**](#mqttclient) object.

### application
Opens an application manager that can be used to manage settings and devices of the application with the ID you provided to the constructor.
```python
handler.application()
```
Returns an [**ApplicationClient**](#applicationclient) object.

## Exceptions
Errors can happen on connection or on some ApplicationClient's methods call, for different reasons:
* Wrong `app_id`, `access_key` or `mqtt_address` were provided to the constructor.
* The machine may not have access to the network/The MQTT server could be down/Firewall restrictions could prevent connection.
* The client process doesn't have system capabilities to open a socket
* The MQTT server uses MQTTS, but the client won't accept the TLS certificate.
* The Application client is not able to get the application or a device.
Errors could also happen when closing connection, in case the disconnection is unexpected. This errors are the most common ones, there are also edges cases not mentioned in this section.
