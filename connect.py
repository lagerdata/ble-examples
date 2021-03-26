"""
Connect by BLEDevice
"""

import asyncio

from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError


async def print_services(ble_address: str):
    device = await BleakScanner.find_device_by_address(ble_address, timeout=20.0)
    if not device:
        raise BleakError(f"A device with address {ble_address} could not be found.")
    async with BleakClient(device) as client:
        svcs = await client.get_services()
        print("Services:")
        for service in svcs:
            print(service)


ble_address = "D9:B7:C3:8C:50:5D"
loop = asyncio.get_event_loop()
loop.run_until_complete(print_services(ble_address))
