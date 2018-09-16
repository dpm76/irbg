import pyb

class Servo(object):

    def __init__(self, pin, timer, channel, freq=50):
    
    	self._pin = pin
        self._timer = pyb.Timer(timer, freq=freq)
        self._channel = self._timer.channel(channel, pyb.Timer.PWM, pin=self._pin, pulse_width=0)
        
        
    def setThrottle(self, throttle):
        
        min = 5.0
        max = 10.0
        
        perc = min + ((max - min) * throttle / 100.0)
        
        self._channel.pulse_width_percent(perc)
        
        
    def cleanup(self):
    
        self._channel.pulse_width(0)
        self._timer.deinit()
        
        self._pin.init(0)

#s = Servo(pyb.Pin.board.D5, 1, 2)
#s.setThrottle(50.0)
#s.cleanup()