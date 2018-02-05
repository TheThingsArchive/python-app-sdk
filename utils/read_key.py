# coding: Latin-1
# Copyright © 2018 The Things Network
# Use of this source code is governed by the
# MIT license that can be found in the LICENSE file.


def read_key(filename):
    with open(filename, "r") as key_file:
        key = key_file.read()
        return key
