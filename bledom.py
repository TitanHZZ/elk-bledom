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

EFFECT_0  = "three color jump"
EFFECT_1  = "seven color jump"
EFFECT_2  = "three color cross fade"
EFFECT_3  = "seven color cross fade"
EFFECT_4  = "red fade"
EFFECT_5  = "green fade"
EFFECT_6  = "blue fade"
EFFECT_7  = "yellow fade"
EFFECT_8  = "cyan fade"
EFFECT_9  = "magenta fade"
EFFECT_10 = "white fade"
EFFECT_11 = "red green cross fade"
EFFECT_12 = "red blue cross fade"
EFFECT_13 = "green blue cross fade"
EFFECT_14 = "seven color strobe flash"
EFFECT_15 = "red strobe flash"
EFFECT_16 = "green strobe flash"
EFFECT_17 = "blue strobe flash"
EFFECT_18 = "yellow strobe flash"
EFFECT_19 = "cyan strobe flash"
EFFECT_20 = "magenta strobe flash"
EFFECT_21 = "white strobe flash"

MODES = {
    EFFECT_0: 0x87,
    EFFECT_1: 0x88,
    EFFECT_2: 0x89,
    EFFECT_3: 0x8a,
    EFFECT_4: 0x8b,
    EFFECT_5: 0x8c,
    EFFECT_6: 0x8d,
    EFFECT_7: 0x8e,
    EFFECT_8: 0x8f,
    EFFECT_9: 0x90,
    EFFECT_10: 0x91,
    EFFECT_11: 0x92,
    EFFECT_12: 0x93,
    EFFECT_13: 0x94,
    EFFECT_14: 0x95,
    EFFECT_15: 0x96,
    EFFECT_16: 0x97,
    EFFECT_17: 0x98,
    EFFECT_18: 0x99,
    EFFECT_19: 0x9a,
    EFFECT_20: 0x9b,
    EFFECT_21: 0x9c
}

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
        assert br >= 0 and br <= 100
        br = bytearray([0x7e, 0x04, 0x01, br, 0x01, 0xff, 0xff, 0x00, 0xef])
        await self.client.write_gatt_char(CHARACTERISTIC_UUID, br, response=True)

    async def set_power(self, power):
        pw = bytearray([0x7e, 0x04, 0x04, 0xf0, 0x00, 0x01, 0xff, 0x00, 0xef] if power else [0x7e, 0x04, 0x04, 0x00, 0x00, 0x00, 0xff, 0x00, 0xef])
        await self.client.write_gatt_char(CHARACTERISTIC_UUID, pw, response=True)

    # async def set_mode(self, mode):
    #     assert mode >= 0x87 and mode <= 0x9c
    #     md = bytearray([0x7e, 0x00, 0x03, mode, 0x03, 0x00, 0x00, 0x00, 0xef])
    #     await self.client.write_gatt_char(CHARACTERISTIC_UUID, md, response=True)

async def main():
    light = ElkBledomLight(DEVICE_ADDR)
    await light.connect()

    # await light.set_color("FF0000")
    # await asyncio.sleep(0.5)
    # await light.set_color("00FF00")
    # await asyncio.sleep(0.5)
    # await light.set_color("0000FF")

    # await asyncio.sleep(1)

    # await light.set_brightness(50)
    # await asyncio.sleep(1)
    # await light.set_brightness(100)

    # await asyncio.sleep(1)

    # await light.set_mode(0x87)

    await light.set_power(False)
    await asyncio.sleep(1)
    await light.set_power(True)

    await light.disconnect()

asyncio.run(main())
