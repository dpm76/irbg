'''
Created on 18/02/2019

@author: david
'''

from sensor.base.i2c import I2C


K = BLACK = 0
G = GREEN = 1
R = RED = 2
Y = YELLOW = 3


class BiColorLedMatrix(I2C):
    '''
    Controller for the Adafruit's Bicolor LED 8x8 Matrix, which uses the HT16K33 chip
    Ref. https://www.adafruit.com/product/902
    '''

    DEFAULT_ADDRESS = 0x70
    
    BLINK_OFF = 0
    BLINK_2HZ = 1
    BLINK_1HZ = 2
    BLINK_HALF_HZ = 3
    
    
    def __init__(self, address=DEFAULT_ADDRESS, channel=1):
        '''
        Constructor

        @param address: I2C address of the device
        @param channel: I2C channel where the device is connected to
        '''
    
        super().__init__(address, channel)
        
        self._displaySetup = 0
        
        
    def start(self):
        '''
        Wakes up the device
        '''
        
        self._writeByte(0x21, 0)
    
    
    def cleanup(self):
        '''
        Shuts the device down
        '''

        self.displayOff()
        self._writeByte(0x20, 0)
        
        
    def clear(self):
        '''
        Clears the screen
        '''
        
        for row in range(0, 16):
        
            self._writeByte(row, 0)
        
    
    def setBlink(self, mode):
        '''
        Set the blink mode
        
        @param mode: Blink mode. See constants BLINK_*
        '''

        self._displaySetup = (self._displaySetup & 0x6) | (mode << 1)
        self._writeByte(0x80 | self._displaySetup, 0)
    
    
    def setDisplayState(self, on):
        '''
        Turns the display on or off
        '''
        
        self._displaySetup = (self._displaySetup & 0xe) | on
        self._writeByte(0x80 | self._displaySetup, 0)
    
        
    def displayOn(self):
        '''
        Set the display on
        '''
        
        self.setDisplayState(True)
        
        
    def displayOff(self):
        '''
        Set the display off 
        '''
        
        self.setDisplayState(False)
        

    def setDim(self, dim):
        '''
        Set the dim level

        @param dim: value between 0 and 15
        '''

        self._writeByte(0xe0 | (dim & 0x0f), 0)

        
    def dump(self, matrix):
        '''
        Dump the matrix into the device's memory.
        It doesn't care about the size of the matrix, because it uses the first 8 rows and first 8
        columns. Whenever smaller the size, it fills in with zeros.
        '''
        
        for row in range(0, 8):
        
            memGreen = 0
            memRed = 0
            
            for col in range(0, 8):
                
                memGreen |= (matrix[row][col] & GREEN) << col
                memRed |= ((matrix[row][col] & RED)>>1) << col
                
            self._writeByte(row * 2, memGreen)
            self._writeByte((row * 2) + 1, memRed)


if __name__ == "__main__":

  from time import sleep

  matrices = [
       [
         [K,K,R,R,R,R,K,K],
         [K,R,K,K,K,K,R,K],
         [R,K,R,K,K,R,K,R],
         [R,K,K,K,K,K,K,R],
         [R,K,R,K,K,R,K,R],
         [R,K,K,R,R,K,K,R],
         [K,R,K,K,K,K,R,K],
         [K,K,R,R,R,R,K,K]
       ],
       [
         [K,K,R,R,R,R,K,K],
         [K,R,R,R,R,R,R,K],
         [R,R,R,R,R,R,R,R],
         [R,R,R,R,R,R,R,R],
         [R,R,R,R,R,R,R,R],
         [R,R,R,R,R,R,R,R],
         [K,R,R,R,R,R,R,K],
         [K,K,R,R,R,R,K,K]
       ],
       [
         [K,K,Y,Y,Y,Y,K,K],
         [K,Y,Y,Y,Y,Y,Y,K],
         [Y,Y,Y,Y,Y,Y,Y,Y],
         [Y,Y,Y,Y,Y,Y,Y,Y],
         [Y,Y,Y,Y,Y,Y,Y,Y],
         [Y,Y,Y,Y,Y,Y,Y,Y],
         [K,Y,Y,Y,Y,Y,Y,K],
         [K,K,Y,Y,Y,Y,K,K]
       ],
       [
         [K,K,G,G,G,G,K,K],
         [K,G,G,G,G,G,G,K],
         [G,G,G,G,G,G,G,G],
         [G,G,G,G,G,G,G,G],
         [G,G,G,G,G,G,G,G],
         [G,G,G,G,G,G,G,G],
         [K,G,G,G,G,G,G,K],
         [K,K,G,G,G,G,K,K],
       ]
   ]

  try:
      led = BiColorLedMatrix(0x70, 1)
      led.start()
      led.setDim(0xf)
      led.setBlink(BiColorLedMatrix.BLINK_OFF)

      for m in matrices:

          led.dump(m)
          led.displayOn()
          sleep(5)
          led.displayOff()

  except:
      led.cleanup()
