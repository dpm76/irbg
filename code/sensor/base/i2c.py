'''
Created on 23/10/2015

@author: david
'''

try:
    import smbus
    
except ImportError:
    
    class smbus(object):
        @staticmethod
        def SMBus(channel):
            raise Exception("smbus module not found!")
            

class I2C(object):
    '''
    Base class for I2C devices
    '''
    
    def __init__(self, address, channel=1):
        '''
        Constructor

        @param address: I2C address of the device
        @param channel: I2C channel where the device is connected to
        '''
        
        self._address = address
        self._bus = smbus.SMBus(channel)
        

    def _readWord(self, regH, regL):

        byteH = self._bus.read_byte_data(self._address, regH)
        byteL = self._bus.read_byte_data(self._address, regL)
    
        word = (byteH << 8) | byteL
        if (byteH & 0x80) != 0:
            word = -(0xffff - word + 1)
    
        return word
    

    def _readWordHL(self, reg):
    
        return self._readWord(reg, reg+1)
    

    def _readWordLH(self, reg):

        return self._readWord(reg+1, reg)
    
    
    def _writeByte(self, reg, byte):
    
        self._bus.write_byte_data(self._address, reg, byte)
    

    def _writeWord(self, regH, regL, word):
    
        byteH = word >> 8
        byteL = word & 0xff
    
        self._bus.write_byte_data(self._address, regH, byteH)
        self._bus.write_byte_data(self._address, regL, byteL)


    def _writeWordHL(self, reg, word):
    
        self._writeWord(reg, reg+1, word)


    def _writeWordLH(self, reg, word):
    
        self._writeWord(reg+1, reg, word)

