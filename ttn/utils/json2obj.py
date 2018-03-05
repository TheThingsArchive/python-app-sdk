# coding: Latin-1
# Copyright © 2018 The Things Network
# Use of this source code is governed by the
# MIT license that can be found in the LICENSE file.


import json
from collections import namedtuple


def _json_object_hook(d):
    return namedtuple("MSG", d.keys())(*d.values())


def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)
