from os.path import exists

class Pwm(object):
    '''
    Encapsulates the PWM-signal generator.
    It uses the sysfs to work
    '''
    
    def __init__(self, chipNum, port):
        '''
        Constructor
        
        @param chipNum: PWM chip number
        
        EHRPWM0 (ePWM0) is pwmchip1
        EHRPWM1 (ePWM1) is pwmchip4
        EHRPWM2 (ePWM2) is pwmchip7
        ECAP0 (eCAP0) is pwmchip0
        
        @param port: PWM Port number. It depends on the concrete machine where the programm will run.
        '''
        
        self._chipNum = chipNum
        self._port = port
        
        #Enable port if it isn't already done
        if not exists("/sys/class/pwm/pwm-{0}:{1}".format(self._chipNum, self._port)):
            f = open("/sys/class/pwm/pwmchip{0}/export".format(self._chipNum), "w")
            f.write(str(self._port))
            f.flush()
            f.close()
            
        #Reset values
        self._period = self.getPeriod()
        if self._period != 0:
            self.stop()
            self.setDuty(0)
        
    
    def setPeriod(self, period):
        '''
        Set the period value. This is the period between pulses.
        
        @param period: nanoseconds
        '''
        
        f = open("/sys/class/pwm/pwm-{0}:{1}/period".format(self._chipNum, self._port), "w")
        f.write(str(int(period)))
        f.flush()
        f.close()
        
        self._period = period
        
        
    def getPeriod(self):
        '''
        Get the period value. This is the period between pulses.
        
        @return: period nanoseconds
        '''
        
        f = open("/sys/class/pwm/pwm-{0}:{1}/period".format(self._chipNum, self._port), "r")
        line = f.readline()
        f.close()
        
        return int(line)
        
        
    def setFreq(self, freq):
        '''
        Set the frequency at pulses are generated
        
        @param freq: Frequency as Hertz
        '''
        
        period = 1000000000.0/freq        
        self.setPeriod(period)
        
        
    def setDuty(self, duty):
        '''
        Set the duty value. This is the time the signal is high within the pulse.
        
        @param duty: nanoseconds
        '''
        
        f = open("/sys/class/pwm/pwm-{0}:{1}/duty_cycle".format(self._chipNum, self._port), "w")
        f.write(str(int(duty)))
        f.flush()
        f.close()
        
        self._duty = duty
        
        
    def setPolarity(self, inversed):
        '''
        Set the polarity of the PWM signal. It can only be changed when the pwm is not started.
        Default value is not inversed.
        
        @param inversed: Boolean value.
        '''
        
        f = open("/sys/class/pwm/pwm-{0}:{1}/polarity".format(self._chipNum, self._port), "w")
        if inversed:
            f.write("inversed")
        else:
            f.write("normal")
        f.flush()
        f.close()
        
        
    def setDutyPerc(self, perc):
        '''
        Set the duty value as a percentage according to the period of the pulse.
        
        @param perc: Percentage value between 0 and 100
        '''
        
        duty = self._period * float(perc) / 100.0
        self.setDuty(duty)
        
        
    def start(self):
        '''
        Starts the PWM-signal generation
        '''
        
        f = open("/sys/class/pwm/pwm-{0}:{1}/enable".format(self._chipNum, self._port), "w")
        f.write("1")
        f.flush()
        f.close()        
        
        
    def stop(self):
        '''
        Stops the PWM-signal generation
        '''
        
        self.setDuty(0)
        
        f = open("/sys/class/pwm/pwm-{0}:{1}/enable".format(self._chipNum, self._port), "w")
        f.write("0")
        f.flush()
        f.close()        

        
        
    def cleanup(self):
        '''
        Frees all using resources
        '''
        
        f = open("/sys/class/pwm/pwmchip{0}/unexport".format(self._chipNum), "w")
        f.write(str(self._port))
        f.flush()
        f.close()
        