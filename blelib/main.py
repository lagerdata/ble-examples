import asyncio
from bleak import BleakScanner, BleakClient

class Client:
    def __init__(self, _client, *, loop):
        self.loop = loop
        self._client = _client

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def read_gatt_char(self, char_specifier):
        return self.loop.run_until_complete(self._client.read_gatt_char(char_specifier))

    def connect(self):
        return self.loop.run_until_complete(self._client.connect())

    def disconnect(self):
        return self.loop.run_until_complete(self._client.disconnect())

    def has_characteristic(self, uuid):
        for service in self._client.services:
            for characteristic in service.characteristics:
                if characteristic.uuid == uuid:
                    return True
        return False

class Central:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self._client = None

    def scan(self, scan_time=5.0, name=None, address=None):
        """
            Scan for devices. If name or address are provided, remove
            devices that do not match.
        """
        devices = self.loop.run_until_complete(BleakScanner.discover(timeout=scan_time))
        if name is not None:
            devices = [device for device in devices if device.name == name]
        if address is not None:
            devices = [device for device in devices if device.address == address]
        return devices

    def connect(self, address):
        return Client(BleakClient(address), loop=self.loop)


def main():
    central = Central()
    # devices = central.scan(name='kGoal', address='F2:E6:41:55:6F:09')
    with central.connect('F2:E6:41:55:6F:09') as client:
        val = client.read_gatt_char('00002a29-0000-1000-8000-00805f9b34fb')
        print('read char: ', val)
        print('has char: ', client.has_characteristic('00002a29-0000-1000-8000-00805f9b34fb'))


if __name__ == '__main__':
    main()
