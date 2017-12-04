from ttn import ApplicationClient
from utils import stubs
import binascii


def test_application_constructor():
    appclient = ApplicationClient('test-python-sdk',
                                  ('ttn-account-v2.suDG-8zvpIFL42r-f6qRcMj'
                                   '_Na5O2Dm_IH8Up6BcrAY'))
    assert hasattr(appclient, 'app_access_key')


def test__application_constructor_token():
    appclient = ApplicationClient(stubs.apptest['appId'],
                                  stubs.apptest['accessToken'])
    assert hasattr(appclient, 'app_access_token')


def test_application_get():
    appclient = ApplicationClient('test-python-sdk',
                                  ('ttn-account-v2.suDG-8zvpIFL42r-f6qRcMj'
                                   '_Na5O2Dm_IH8Up6BcrAY'))
    app = appclient.get()
    assert app.app_id == 'test-python-sdk'


def test_application_devices():
    appclient = ApplicationClient('test-python-sdk',
                                  ('ttn-account-v2.suDG-8zvpIFL42r-f6qRcMj'
                                   '_Na5O2Dm_IH8Up6BcrAY'))
    devices = appclient.devices()
    assert not devices


def test_set_payload_format():
    appclient = ApplicationClient('test-python-sdk',
                                  ('ttn-account-v2.suDG-8zvpIFL42r-f6qRcMj'
                                   '_Na5O2Dm_IH8Up6BcrAY'))
    appclient.set_payload_format('payloadformat')
    app = appclient.get()
    assert app.payload_format == 'payloadformat'


def test_set_custom_payload():
    appclient = ApplicationClient('test-python-sdk',
                                  ('ttn-account-v2.suDG-8zvpIFL42r-f6qRcMj'
                                   '_Na5O2Dm_IH8Up6BcrAY'))
    appclient.set_custom_payload_functions(validator="validator",
                                           decoder="decoder")
    app = appclient.get()
    assert app.payload_format == "custom" and app.decoder == "decoder" and \
        app.validator == "validator"


def test_set_register_on_join_access_key():
    appclient = ApplicationClient('test-python-sdk',
                                  ('ttn-account-v2.suDG-8zvpIFL42r-f6qRcMj'
                                   '_Na5O2Dm_IH8Up6BcrAY'))
    appclient.set_register_on_join_access_key('register')
    app = appclient.get()
    assert app.register_on_join_access_key == 'register'


def test_register_device():
    appclient = ApplicationClient('test-python-sdk',
                                  ('ttn-account-v2.suDG-8zvpIFL42r-f6qRcMj'
                                   '_Na5O2Dm_IH8Up6BcrAY'))
    appclient.register_device("foo", stubs.devicetest)


def test_device():
    appclient = ApplicationClient('test-python-sdk',
                                  ('ttn-account-v2.suDG-8zvpIFL42r-f6qRcMj'
                                   '_Na5O2Dm_IH8Up6BcrAY'))
    device = appclient.device('foo')
    assert device.dev_id == "foo"


def test_update_device():
    appclient = ApplicationClient('test-python-sdk',
                                  ('ttn-account-v2.suDG-8zvpIFL42r-f6qRcMj'
                                   '_Na5O2Dm_IH8Up6BcrAY'))
    update = {
        "devEui": "1100223344556677",
    }
    appclient.update_device('foo', update)
    dev = appclient.device('foo')
    assert dev.lorawan_device.dev_eui == binascii.unhexlify("1100223344556677")


def test_delete_device():
    appclient = ApplicationClient('test-python-sdk',
                                  ('ttn-account-v2.suDG-8zvpIFL42r-f6qRcMj'
                                   '_Na5O2Dm_IH8Up6BcrAY'))
    appclient.delete_device("foo")
    devices = appclient.devices()
    assert not devices
