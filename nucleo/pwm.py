import pyb

class Pwm(object):

    def __init__(self, pin, timer, channel, freq):
    
    	self._pin = pin
        self._timer = pyb.Timer(timer, freq=freq)
        self._channel = self._timer.channel(channel, pyb.Timer.PWM, pin=self._pin, pulse_width=0)
        
        
    def setDutyPerc(self, dutyPerc):
        
        self._channel.pulse_width_percent(dutyPerc)
        
        
    def cleanup(self):
    
        self._channel.pulse_width(0)
        self._timer.deinit()
        
        self._pin.init(0)

if __name__ == "__main__":
    
    import utime
    
    pwm = Pwm(pyb.Pin.board.D10, 4, 3, 880.0)
    for x in range(20):
        for i in range (4):
            pwm.setDutyPerc(50.0)
            utime.sleep_ms(100)
            pwm.setDutyPerc(0)
            utime.sleep_ms(50)
            
        utime.sleep_ms(200)

    pwm.cleanup()
    