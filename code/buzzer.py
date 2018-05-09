from pwm import Pwm
from time import sleep

class Buzzer(object):
    '''
    Makes a buzzer playing notes
    '''

    def __init__(self, port):
        '''
        Constructor
        
        @param port: PWM port where the buzzer is connected to
        '''
        
        self._pwm = Pwm(port)
        

    def playNote(self, freq, time):
        '''
        Plays a frequency sound during a time
        
        @param freq: Frequency of the played sound. If this value is 0 a silence will be performed.
        @param time: Time the sound will be played
        '''
        
        if freq > 0.0:
            self._pwm.setFreq(freq)
            self._pwm.setDutyPerc(50)
            self._pwm.start()
            sleep(time)
            self._pwm.setDuty(0)
            self._pwm.stop()
        else:
            sleep(time)
        

    def cleanup(self):
        '''
        Frees all using resources
        '''
        
        self._pwm.cleanup()

