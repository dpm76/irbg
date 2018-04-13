from os.path import exists

class Gpio(object):
    '''
    Encapsulates the GPIO logic
    '''
    
    IN = "in"   #In direction 
    OUT = "out" #Out direction
    
    HIGH = True #High value
    LOW = False #Low value

    def __init__(self, port, direction):
        '''
        Constructor
        @param port: port number, this port must be enabled as GPIO previously
        @param direction: @see Gpio.IN @see Gpio.OUT
        '''
    
        self._port = port

        #Enable port if it doesn't exist
        if not exists("/sys/class/gpio/gpio{0}".format(self._port)):
            f = open("/sys/class/gpio/export","w")
            f.write(str(self._port))
            f.flush()
            f.close()
        
        #enable direction
        f = open("/sys/class/gpio/gpio{0}/direction".format(self._port),"w")
        f.write(direction)
        f.flush()
        f.close()
        
        #open value file
        openMode = "r" if direction == Gpio.IN else "w"
        self._value = open("/sys/class/gpio/gpio{0}/value".format(self._port), openMode)


    def setValue(self, value):
        '''
        Set the port value when it works as output mode.
        @param value: True or @see Gpio.HIGH and False or Gpio.LOW values are allowed
        '''

        self._value.write('1' if value else '0')
        self._value.flush()
        
        
    def getValue(self):
        '''
        Reads the current port value
        @returns : Curent port value
        '''
        
        self._value.seek(0)
        value = self._value.read()

        return value and value[0] == '1'
        
        
    def cleanup(self):
        '''
        Closes the port
        '''

        self._value.close()
    
        f = open("/sys/class/gpio/unexport","w")
        f.write(str(self._port))
        f.flush()
        f.close()
