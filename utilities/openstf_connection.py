# -*- coding: utf-8 -*-

import argparse
from openstf_api import OpenSTF
from dotenv import load_dotenv
import os
import sys

"""Load environment variables from .env"""
dotenv_path = (os.path.join(sys.path[0], '../.env'))
load_dotenv(dotenv_path)

"""Define parser for CLI interaction"""
parser = argparse.ArgumentParser(
    description='Determine how to interact with STF')
parser.add_argument("--connect", nargs='?',
                    default=None, help="Control a device")
parser.add_argument("--disconnect", nargs='?',
                    default=None, help="Disconnect from device")
parser.add_argument("--serial", action="store_true",
                    help="Get a random devices serial number")
parser.add_argument("--random", action="store_true",
                    help="Get a random devices & return URL")

"""Build connect to Open STF server"""
stf_farm = OpenSTF(url=os.environ.get("STF_URL"),
                   token=os.environ.get("STF_TOKEN"))

args = parser.parse_args()

if args.serial:
    device_serial = stf_farm.get_random_device()
    print device_serial
elif args.connect:
    if args.connect is None:
        raise Exception('Please provide a serial number')
    else:
        print stf_farm.get_device_url(serial=args.connect)
elif args.disconnect:
    if args.disconnect is None:
        raise Exception('Please provide a serial number')
    else:
        stf_farm.disconnect_device(serial=args.disconnect)
elif args.random:
    device_url = stf_farm.get_device_url()
    print device_url
