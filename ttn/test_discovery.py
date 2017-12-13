# coding: Latin-1
# Copyright © 2017 The Things Network
# Use of this source code is governed by the
# MIT license that can be found in the LICENSE file.


from ttn import DiscoveryClient
from utils import stubs


def test_constructor_discovery():
    discovery = DiscoveryClient()
    assert hasattr(discovery, "client")


def test_get_by_app_id():
    discovery = DiscoveryClient()
    res = discovery.get_by_app_id("test-python-sdk")
    assert res.id == "ttn-handler-eu"


def test_get():
    discovery = DiscoveryClient()
    res = discovery.get("handler", "ttn-handler-eu")
    assert res


def test_get_all():
    discovery = DiscoveryClient()
    res = discovery.get_all("handler")
    assert res
