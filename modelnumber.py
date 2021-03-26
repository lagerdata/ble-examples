import asyncio
from bleak import BleakScanner, BleakClient
from bleak.exc import BleakError

MODEL_NBR_UUID = "00002a24-0000-1000-8000-00805f9b34fb"

async def run():
    devices = await BleakScanner.discover()
    for d in devices:
        try:
            async with BleakClient(d, timeout=3) as client:
                try:
                    model_number = await client.read_gatt_char(MODEL_NBR_UUID)
                except (EOFError, BleakError):
                    print(f'Could not connect to {d}')
                else:
                    print(f"{d.name} Model Number: {''.join(map(chr, model_number))}")
        except (BleakError, asyncio.TimeoutError):
            print(f'Could not connect to {d}')

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
