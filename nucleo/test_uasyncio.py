import pyb
import uasyncio as asyncio

async def killer(duration):
    await asyncio.sleep(duration)

async def toggle(objLED, time_ms):
    while True:
        await asyncio.sleep_ms(time_ms)
        objLED.toggle()

def testLeds(duration=0):
    loop = asyncio.get_event_loop()
    duration = int(duration)
    if duration > 0:
        print("Flash LEDs for {:3d} seconds...".format(duration))
    else:
        print("Flash LEDs forever...")
    leds = [pyb.LED(x) for x in range(1,4)]  # Initialise all board LEDs
    for x, led in enumerate(leds):           # Create a coroutine for each LED
        t = int((0.2 + x/2) * 1000)
        loop.create_task(toggle(leds[x], t))
    if duration > 0:
        loop.run_until_complete(killer(duration))
        loop.close()
        for led in leds:
            led.off()
    else:
        loop.run_forever()

def run():
    testLeds()

if __name__ == "__main__":
    run()
