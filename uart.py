"""
UART Service
-------------
An example showing how to write a simple program using the Nordic Semiconductor
(nRF) UART service.
"""

import asyncio

from bleak import BleakScanner, BleakClient
from bleak.backends.scanner import AdvertisementData
from bleak.backends.device import BLEDevice
from bleak.exc import BleakError

UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

async def uart_terminal():
    def handle_disconnect(_: BleakClient):
        print("Device was disconnected, goodbye.")
        # cancelling all tasks effectively ends the program
        for task in asyncio.all_tasks():
            task.cancel()

    def handle_rx(_: int, data: bytearray):
        print(f"received: {data.decode()}", end='')

    device = await BleakScanner.find_device_by_address('E4:B6:8E:F3:A0:2E', timeout=20.0)
    if not device:
        raise BleakError('Device not found')

    async with BleakClient(device, disconnected_callback=handle_disconnect) as client:
        await client.start_notify(UART_TX_CHAR_UUID, handle_rx)
        svcs = await client.get_services()
        print("Services:")
        for service in svcs:
            print(service)

        data = b'Hello!\n'
        await client.write_gatt_char(UART_RX_CHAR_UUID, data, True)
        print("sent:", data)
        await asyncio.sleep(5)


try:
    asyncio.run(uart_terminal())
except asyncio.CancelledError:
    pass