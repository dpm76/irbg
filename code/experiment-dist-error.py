#!/usr/bin/python3

from experiment import ExperimentApp

from ultrasonic import Ultrasonic


class DistanceErrorApp(ExperimentApp):

    GPIO_TRIGGER = 66 #P8.7
    GPIO_ECHO    = 67 #P8.8

    def __init__(self):
    
        super().__init__("Distance Error")
        self.setPollingPeriod(1)
        
        self._meter = Ultrasonic(DistanceErrorApp.GPIO_TRIGGER, DistanceErrorApp.GPIO_ECHO)


    def getValues(self):

        distRead = self._meter.read()
        if distRead == Ultrasonic.OUT_OF_RANGE:
            distRead = 0
        
        return (100, int(distRead))
        
        
    def cleanup(self):
    
        self._meter.cleanup()



if __name__ == '__main__':

    DistanceErrorApp().run()
