# coding: Latin-1
# Copyright © 2018 The Things Network
# Use of this source code is governed by the
# MIT license that can be found in the LICENSE file.

from setuptools import find_packages, setup

import io

with io.open("README.rst", encoding="utf-8") as f:
    long_description = f.read()

setup(name="ttn",
      version="2.1.1",
      description="The Things Network Client",
      long_description = long_description,
      url = "https://github.com/TheThingsNetwork/python-app-sdk",
      author="Emmanuelle Lejeail",
      author_email="emmanuelle@thethingsindustries.com",
      license="MIT",
      packages=find_packages(),
      install_requires=[
          "paho-mqtt",
          "events",
          "grpcio",
          "python-jose",
          # packages which need to be imported to make gRPC work
          "protobuf",
          "google-api-python-client",
          "google-cloud"
      ],
      zip_safe=False)
