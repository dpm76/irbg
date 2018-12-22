from gpio import Gpio
import time

class Ultrasonic(object):

    PULSE2CM = 17241.3793 # cm/s

    def __init__(self, triggerPort, echoPort):
        '''
        Constructor
        @param triggerPort: Port number of the trigger signal
        @param echoPort: Port number of the echo port
        '''

        #Configure ports	
        self._trigger = Gpio(triggerPort, Gpio.OUT)
        self._trigger.setValue(Gpio.LOW)

        self._echo = Gpio(echoPort, Gpio.IN)

        time.sleep(2)

		
    def read(self):
        '''
        Measures distance
        @return: Distance as centimeters
        '''
	
        self._trigger.setValue(Gpio.HIGH)
        time.sleep(0.001)
        self._trigger.setValue(Gpio.LOW)

        while self._echo.getValue() == Gpio.LOW:
            pass
        pulseStart = time.time()	

        while self._echo.getValue() == Gpio.HIGH:
            pass
        pulseEnd = time.time()

        pulseDuration = pulseEnd-pulseStart
        dist = round(pulseDuration * Ultrasonic.PULSE2CM, 0) #cm

        return dist


    def cleanup(self):
        '''
        Frees ressources
        '''

        self._trigger.cleanup()
        self._echo.cleanup()

		
if __name__ == '__main__':

    GPIO_TRIGGER = 66 #P8.7
    GPIO_ECHO    = 67 #P8.8

    try:
        print("Press Ctrl+C to finish")
        meter = Ultrasonic(GPIO_TRIGGER, GPIO_ECHO)

        while True:
            dist = meter.read()
            print("~ {0} cm".format(dist))
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nCtrl+C pressed.")

    finally:
        print("Bye!")
        meter.cleanup()
