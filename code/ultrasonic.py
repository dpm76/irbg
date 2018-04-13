from gpio import Gpio
import time

class Ultrasonic(object):

	def __init__(self):

                #Configure ports	
                self._trigger = Gpio(66, Gpio.OUT) #P8.7
                self._trigger.setValue(Gpio.LOW)

                self._echo = Gpio(69, Gpio.IN) #P8.9

		time.sleep(2)

		
	def read(self):
		
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

            self._trigger.cleanup()
            self._echo.cleanup()

		
if __name__ == '__main__':

	try:
		meter = Ultrasonic()
		dist = meter.read()
	
		print("~ {0} cm".format(dist))
	
	finally:
		meter.cleanup()
