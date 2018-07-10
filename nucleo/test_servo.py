class Servo(object):

    def __init__(self, pin, timer, channel, freq=50):
    
    	self._pin = pin
    	afList = self._pin.af_list()
    	
    	numAf = len(afList)
    	
    	# Search timer function
    	index = 0
    	if numAf != 0:

    	    while index < numAf and "TIM" not in afList[index].name():
    	        index += 1
    	        
    	if numAf == 0 or index == numAf:
    	
    	    raise Exception("Pin {0} hasn't any alternate function.".format(self._pin.name()))
    	
    	af = afList[index]
    	afName = af.name()
    	channel = int(afName[2])
    	timer = int(afName[7:])
    	
    	self._pin.init(pyb.Pin.AF_PP, af=af.index())
    	
        self._timer = pyb.Timer(timer, freq=freq)
        self._channel = self._timer.channel(channel, pyb.Timer.PWM, pin=self._pin, pulse_width=0)
        
        
        
        
    def cleanup(self):
    
        self._channel.pulse_width(0)
        self._timer.deinit()
        
        self._pin.init(0, af=-1)
