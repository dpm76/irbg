from gpio import Gpio
import time

class Ultrasonic(object):

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
        dist = round(pulseDuration * 17241.3793, 0) #cm

        return dist


    def cleanup(self):
        '''
        Frees ressources
        '''

        self._trigger.cleanup()
        self._echo.cleanup()

		
if __name__ == '__main__':

    try:
        meter = Ultrasonic(66, 69) #P8.7, P8.9
        dist = meter.read()
	
        print("~ {0} cm".format(dist))

    finally:
        meter.cleanup()
