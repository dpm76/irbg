from time import sleep

import pyb

def main():

    leds = [pyb.LED(1), pyb.LED(2), pyb.LED(3)]

    index = 0
    incrementer = 1

    while True:
        for led in leds:
            led.off()
        
        leds[index].on()

        index = index + incrementer    
        if index < 0 or index == len(leds):
            incrementer *= -1
            index = index + incrementer
            index = index + incrementer
    
        sleep(0.15)

if __name__ == "__main__":
    main()
