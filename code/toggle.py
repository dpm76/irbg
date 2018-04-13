from gpio import Gpio
from time import sleep

led = Gpio(27, Gpio.OUT) #P8.17
key = Gpio(65, Gpio.IN) #P8.18

try:

    light = Gpio.LOW
    led.setValue(light)
    
    lastKeyState = Gpio.LOW
    print("Ready.\nPress toggle key to change led state or Ctrl+C to exit.")

    while True:
    
        keyState = key.getValue()
        if lastKeyState != keyState and keyState == Gpio.HIGH:
            light = not light
            led.setValue(light)
            print("Led state changed to {0}.".format("ON" if light else "OFF"))
            
        lastKeyState = keyState
            
        sleep(0.2)

except KeyboardInterrupt:

    print("\nBye!")

finally:
    led.setValue(Gpio.LOW)
    led.cleanup()
    key.cleanup()
