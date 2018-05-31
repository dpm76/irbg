from pwm import Pwm

class Servo(object):
    '''
    Servo driver class
    '''
    
    PERIOD = 20000000
    MIN_DUTY = 1000000
    NEUTRAL_DUTY = 1500000
    MAX_DUTY = 2000000
    
    def __init__(self, port):
        '''
        Constructor.
        Inits servo to neutral value, but a different value can be set after construtor call.
        
        @param port: PWM port the server is connected to
        '''
        
        self._pwm = Pwm(port)
        self._pwm.setPeriod(Servo.PERIOD)
        self._pwm.setDuty(Servo.NEUTRAL_DUTY)
        
        
    def start(self):
        '''
        Starts the servo
        '''
        
        self._pwm.start()
        
        
    def stop(self):
        '''
        Stops using servo
        '''
        
        self._pwm.stop()
        
        
    def cleanup(self):
        '''
        Frees used resources
        '''

        self._pwm.cleanup()
        
        
    def setValue(self, perc):
        '''
        Set a custom value
        
        @param perc: Percentage value between 0 and 100
        '''
        
        if 0 <= perc <= 100:
        
            duty = Servo.MIN_DUTY + (Servo.MAX_DUTY - Servo.MIN_DUTY) * perc / 100.0
            self._pwm.setDuty(duty)        
        
        
    def setNeutral(self):
        '''
        Set value to neutral
        '''
        
        self._pwm.setDuty(Servo.NEUTRAL_DUTY)
        
        
    def setMin(self):
        '''
        Set value to minimum
        '''
        
        self._pwm.setDuty(Servo.MIN_DUTY)
        
        
    def setMax(self):
        '''
        Set value to maximum
        '''
        
        self._pwm.setDuty(Servo.MAX_DUTY)
