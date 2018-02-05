# coding: Latin-1
# Copyright © 2018 The Things Network
# Use of this source code is governed by the
# MIT license that can be found in the LICENSE file.


def split_address(address):
    if ":" in address:
        split = address.split(":")
        address = split[0]
        port = int(split[1])
        return {"address": address, "port": port}
    else:
        return {"address": address}
