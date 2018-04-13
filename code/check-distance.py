from ultrasonic import Ultrasonic
from blink import Blinker
from gpio import Gpio
from time import sleep

MIN_DELAY = 0.05
MAX_DELAY = 1.0
MAX_DIST = 300.0
DELAY_COEF = MAX_DELAY / MAX_DIST

def calculateDelay(dist):
    '''
    Calculates the delay according to a distance.
    @param dist: Distance
    '''
    
    delay = 0.0
    
        
    if dist < MAX_DIST:
    
        delay = dist * DELAY_COEF
        
        if delay < MIN_DELAY:
           delay = MIN_DELAY
        
    else:
    
        delay = MAX_DELAY
        
        
    return delay
        

def main():
    '''
    Makes a LED to blink according to the distance meassured
    by an ultrasonic sensor.
    Finish when user press a toggle key.
    '''    
    
    blinker = Blinker(27, MAX_DELAY) #P8.17
    ultrasonic = Ultrasonic()
    key = Gpio(65, Gpio.IN) #P8.18
    
    try:

        print("Ready. Press toggle key to start.")

        #Wait for key down event
        while key.getValue() == Gpio.LOW:

            sleep(0.2)

        #Wait for key up event
        while key.getValue() == Gpio.HIGH:

            sleep(0.2)
    
        print("Started. Press toggle key again to finish.")
        blinker.start()
        
        while key.getValue() == Gpio.LOW:
            dist = ultrasonic.read()
            delay = calculateDelay(dist)
            blinker.setDelay(delay)
            sleep(0.2)

        print("Bye!")
        
    finally:
        key.cleanup()
        blinker.stop()
        blinker.cleanup()
        ultrasonic.cleanup()
    
    
if __name__ == "__main__":

    main()
    
