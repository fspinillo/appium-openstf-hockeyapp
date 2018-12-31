# -*- coding: utf-8 -*-

import requests
import random


class OpenSTF:

    def __init__(self, url, token):
        self.base = 'http://{0}/api/v1/'.format(url)
        self.token = token
        self.device_url = 'http://{0}/api/v1/devices'.format(url)
        self.user_url = 'http://{0}/api/v1/user'.format(url)
        self.headers = {"Authorization": "Bearer {0}".format(token)}

    def devices(self):
        """Get list of devices in OpenSTF Farm"""
        device_list = requests.get(self.device_url, headers=self.headers)
        if device_list.status_code == '401':
            raise Exception('Bad Credentials')

        return device_list.json()

    def device(self, serial=None):
        """Gets a specific device in the farm"""
        if serial is None:
            raise Exception("Serial cannot be empty. Please provide a device "
                            "serial number to connect to.")
        get_device = requests.get('{0}{1}'.format(
            self.device_url, serial), headers=self.headers)

        if get_device.status_code == 404:
            raise Exception('Device not found')

    def connect_device(self, serial=None):
        """Connects to a device"""
        if serial is None:
            raise Exception('Serial cannot be empty. Please provide a device '
                            'serial number to connect to.')
        header = {
            'Authorization': 'Bearer {0}'.format(self.token),
            'content-type': 'application/json'
        }
        device_connect = requests.post(
            '{URL}/devices'.format(URL=self.user_url), headers=header,
            json={'serial': '{0}'.format(serial)})

        if device_connect.status_code == 404:
            raise Exception('Device not found')
        elif device_connect.status_code == 403:
            raise Exception('Device is being used or not available')

    def connect_url(self, serial=None):
        """Retrieves the remote connect url for ADB"""
        if serial is None:
            raise Exception('Serial cannot be empty. Please provide a device '
                            'serial number to connect to.')

        remote_url = requests.post('{URL}/devices/{SERIAL}/remoteConnect'.format(
            URL=self.user_url, SERIAL=serial), headers=self.headers)

        if remote_url.status_code == 200:
            remote = remote_url.json()
            return remote['remoteConnectUrl']
        elif remote_url.status_code == 404:
            raise Exception('Device not found')

    def disconnect_device(self, serial=None):
        """Disconnects from the device"""
        if serial is None:
            raise Exception('Serial cannot be empty. Please provide a device '
                            'serial number to connect to.')

        """disconnect ADB service"""
        requests.delete(
            '{URL}/devices/{SERIAL}/remoteConnect'.format(URL=self.user_url,
                                                          SERIAL=serial),
            headers=self.headers)

        """disconnect from device"""
        requests.delete(
            '{URL}/devices/{SERIAL}/'.format(URL=self.user_url, SERIAL=serial),
            headers=self.headers)

    def get_random_device(self):
        """Gets a random device and returns the serial number"""
        device_list = self.devices()
        devices = device_list['devices']
        device_ready = False
        while device_ready is False:
            random_device = devices[random.randrange(0, len(devices))]
            if random_device['present'] is True:
                device_ready = True

        serial = str(random_device['serial'])
        return serial

    def get_device_url(self, serial=None):
        if serial is None:
            serial = self.get_random_device()

        self.connect_device(serial=serial)
        device_url = self.connect_url(serial=serial)
        return device_url
