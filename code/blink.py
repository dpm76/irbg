import time
from threading import Thread
from gpio import Gpio

class Blinker(object):
    '''
    Makes a LED to blink
    '''

    def __init__(self, port, delay = 0.1):
        '''
        Constructor
        @param port: GPIO port number where the LED is connected to
        @param delay: Time the LED is on and off. Default 0.1s
        '''

        self._port = Gpio(port, Gpio.OUT)
        self._delay = delay
        self._isRunning = False
        self._doBlinkThread = None


    def start(self):
        '''
        Starts the LED to be blinking
        '''

        if self._doBlinkThread == None or not self._doBlinkThread.isAlive():
  
            self._isRunning = True
            self._doBlinkThread = Thread(target=self._doBlink)
            self._doBlinkThread.start()


    def stop(self):
        '''
        Stops the LED blinking
        '''

        self._isRunning = False
        if self._doBlinkThread != None and self._doBlinkThread.isAlive():

            self._doBlinkThread.join()


    def setDelay(self, delay):
        '''
        Set the time the LED is on and off
        @param delay: seconds
        '''

        self._delay = delay


    def _doBlink(self):
        '''
        Thread action to be the LED blinking
        '''
        
        status = True

        while self._isRunning:
    
            self._port.setValue(status)
            status = not status
            time.sleep(self._delay)

        self._port.setValue(False)


    def cleanup(self):
        '''
        Frees ressources
        '''

        self._port.cleanup()


if __name__ == "__main__":

    blinker = Blinker(27) #P8.17
    try:
        blinker.start()
        time.sleep(3)
        blinker.setDelay(0.02)
        time.sleep(3)
        blinker.stop()
    finally:
        blinker.cleanup()
