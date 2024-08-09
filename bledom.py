# usefull resources:
# https://github.com/TheSylex/ELK-BLEDOM-bluetooth-led-strip-controller
# https://github.com/FergusInLondon/ELK-BLEDOM
# https://github.com/8none1/elk-bledob
# https://github.com/arduino12/ble_rgb_led_strip_controller

import asyncio
from asyncio.tasks import sleep
from bleak import BleakClient

DEVICE_ADDR = "FF:FF:10:FF:89:EC"
SERVICE_UUID = "0000fff0-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_UUID = "0000fff3-0000-1000-8000-00805f9b34fb"
MAX_CONNECTIONS = 20

class ElkBledomLight:
    def __init__(self, address):
        self.client = None
        self.address = address
        self.connected = False

    async def connect(self):
        connection_attempts = 0

        while connection_attempts < MAX_CONNECTIONS and not self.connected:
            try:
                self.client = BleakClient(timeout=1.5, address_or_ble_device=self.address)
                await self.client.connect()
                print(f"Connected to ELK_BLEDOM rgb strip with address {self.address}!")
                self.connected = True

                await self.set_free()
            except:
                pass

            connection_attempts += 1

        if connection_attempts >= MAX_CONNECTIONS:
            print(f"Max connection attempts reached for {self.address}.")
            exit(1)

    async def disconnect(self):
        if self.connected:
            print(f"Disconnecting gracefully from ELK-BLEDOM with address {self.address}!")
            await self.client.disconnect()

    async def set_color(self, clr):
        color = bytearray([0x7e, 0x07, 0x05, 0x03, int(clr[0:2], 16), int(clr[2:4], 16), int(clr[4:6], 16), 0x10, 0xef])
        await self.client.write_gatt_char(CHARACTERISTIC_UUID, color, response=True)

    async def set_brightness(self, br):
        br = bytearray([0x7e, 0x04, 0x01, br, 0x01, 0xff, 0x02, 0x01, 0xef])
        await self.client.write_gatt_char(CHARACTERISTIC_UUID, br, response=True)

    # async def set_power(self, power):
    #     pw = bytearray([0x7e, 0x00, 0x04, 0xf0, 0x00, 0x01, 0xff, 0x00, 0xef] if power else [0x7e, 0x00, 0x04, 0x00, 0x00, 0x00, 0xff, 0x00, 0xef])
    #     await self.client.write_gatt_char(CHARACTERISTIC_UUID, pw, response=True)

async def main():
    light = ElkBledomLight(DEVICE_ADDR)
    await light.connect()

    await light.set_color("FF0000")
    await asyncio.sleep(0.5)
    await light.set_color("00FF00")
    await asyncio.sleep(0.5)
    await light.set_color("0000FF")

    await asyncio.sleep(1)

    await light.set_brightness(50)
    await asyncio.sleep(1)
    await light.set_brightness(100)

    await asyncio.sleep(1)

    # await light.set_power(False)
    # await asyncio.sleep(1)
    # await light.set_power(True)

    await light.disconnect()

# Run the async main function
asyncio.run(main())
