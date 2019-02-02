from gpio import Gpio
import time

class ReadGpioException(Exception):
    pass

class Ultrasonic(object):

    PULSE2CM = 17241.3793 # cm/s
    MAX_RANGE = 3500 # cm
    OUT_OF_RANGE = 0xffffffff

    def __init__(self, triggerPort, echoPort, nSamples = 5):
        '''
        Constructor
        @param triggerPort: Port number of the trigger signal
        @param echoPort: Port number of the echo port
        @param nSamples: Number of samples to measure the distance
        '''

        self._nSamples = nSamples

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

        MAX_POLL = 1000
        i = 0
        dist = 0

        while i < self._nSamples and dist != Ultrasonic.OUT_OF_RANGE:
            self._trigger.setValue(Gpio.HIGH)
            time.sleep(0.001)
            self._trigger.setValue(Gpio.LOW)

            #TODO: use system's poll mechanism or event to wait for GPIO-level change
            nPoll = 0
            while nPoll < MAX_POLL and self._echo.getValue() == Gpio.LOW:
                nPoll += 1

            if nPoll == MAX_POLL:
                raise ReadGpioException("Max poll reached: waiting for echo HIGH")            

            pulseStart = time.time()

            nPoll = 0
            while nPoll < MAX_POLL and self._echo.getValue() == Gpio.HIGH:
                nPoll += 1

            if nPoll == MAX_POLL:
                raise ReadGpioException("Max poll reached: waiting for echo LOW")

            pulseEnd = time.time()

            pulseDuration = pulseEnd-pulseStart
            distSample = round(pulseDuration * Ultrasonic.PULSE2CM, 0) #cm

            if distSample < Ultrasonic.MAX_RANGE:
                dist = (dist + distSample) / 2.0 if i != 0 else distSample
            else:
                dist = Ultrasonic.OUT_OF_RANGE
            
            i+=1

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
            try:
                dist = meter.read()
                if dist != Ultrasonic.OUT_OF_RANGE:
                    print("~ {0:.3f} cm".format(dist))
                else:
                    print("Out of range!")
            except ReadGpioException:
                print("I couldn't read GPIO!")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nCtrl+C pressed.")

    finally:
        print("Bye!")
        meter.cleanup()
