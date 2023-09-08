from utime import sleep_ms
from machine import I2C, Pin
from micropython import const

class Bmp180(object):
    '''
    Interface for the BMP-180 sensor.
    Derivated from the BMP-085 sensor of the pycomms library
    '''

    # Operating Modes
    MODE_ULTRALOWPOWER     = const(0)
    MODE_STANDARD          = const(1)
    MODE_HIGHRES           = const(2)
    MODE_ULTRAHIGHRES      = const(3)

    # BMP085 Registers
    REG_CAL_AC1           = const(0xAA)  # R   Calibration data (16 bits)
    REG_CAL_AC2           = const(0xAC)  # R   Calibration data (16 bits)
    REG_CAL_AC3           = const(0xAE)  # R   Calibration data (16 bits)
    REG_CAL_AC4           = const(0xB0)  # R   Calibration data (16 bits)
    REG_CAL_AC5           = const(0xB2)  # R   Calibration data (16 bits)
    REG_CAL_AC6           = const(0xB4)  # R   Calibration data (16 bits)
    REG_CAL_B1            = const(0xB6)  # R   Calibration data (16 bits)
    REG_CAL_B2            = const(0xB8)  # R   Calibration data (16 bits)
    REG_CAL_MB            = const(0xBA)  # R   Calibration data (16 bits)
    REG_CAL_MC            = const(0xBC)  # R   Calibration data (16 bits)
    REG_CAL_MD            = const(0xBE)  # R   Calibration data (16 bits)
    REG_CONTROL           = const(0xF4)
    REG_TEMPDATA          = const(0xF6)
    REG_PRESSUREDATA      = const(0xF6)
    CMD_READTEMP          = const(0x2E)
    CMD_READPRESSURE      = const(0x34)
    
    BYTE_ORDER = "big"


    def __init__(self, channel=0, sclPin=18, sdaPin=19, address = 0x77, mode = 1):
    
        # Private Fields
        _ac1 = 0
        _ac2 = 0
        _ac3 = 0
        _ac4 = 0
        _ac5 = 0
        _ac6 = 0
        _b1 = 0
        _b2 = 0
        _mb = 0
        _mc = 0
        _md = 0
    
        self._i2c = I2C(channel, scl=Pin(sclPin), sda=Pin(sdaPin))
        self._address = address

        # Make sure the specified mode is in the appropriate range
        if ((mode < 0) or (mode > 3)):
            self._mode = Bmp180.MODE_STANDARD
        else:
            self._mode = mode
            
        # Read the calibration data
        self._readCalibrationData()
        
        
    def _write(self, reg, buffer):
    
        self._i2c.writeto_mem(self._address, reg, bytes(buffer))
        
        
    def _readSInt(self, reg):
    
        bytes = self._i2c.readfrom_mem(self._address, reg, 2)
        data = int.from_bytes(bytes, Bmp180.BYTE_ORDER, False)
        if data > 32767:
            data = data - 65536

        return data
        
        
    def _readUInt(self, reg):
    
        bytes = self._i2c.readfrom_mem(self._address, reg, 2)
        data = int.from_bytes(bytes, Bmp180.BYTE_ORDER, False)

        return data
        
    def _readUByte(self, reg):
    
        data =  int.from_bytes(self._i2c.readfrom_mem(self._address, reg, 1), Bmp180.BYTE_ORDER, False)

        return data


    def _readCalibrationData(self):
        # Reads the calibration data from the IC
        self._ac1 = self._readSInt(Bmp180.REG_CAL_AC1)
        self._ac2 = self._readSInt(Bmp180.REG_CAL_AC2)
        self._ac3 = self._readSInt(Bmp180.REG_CAL_AC3)
        self._ac4 = self._readUInt(Bmp180.REG_CAL_AC4)
        self._ac5 = self._readUInt(Bmp180.REG_CAL_AC5)
        self._ac6 = self._readUInt(Bmp180.REG_CAL_AC6)
        self._b1  = self._readSInt(Bmp180.REG_CAL_B1)
        self._b2  = self._readSInt(Bmp180.REG_CAL_B2)
        self._mb  = self._readSInt(Bmp180.REG_CAL_MB)
        self._mc  = self._readSInt(Bmp180.REG_CAL_MC)
        self._md  = self._readSInt(Bmp180.REG_CAL_MD)

    def readRawTemp(self):
        # Reads the raw (uncompensated) temperature from the sensor
        self._write(Bmp180.REG_CONTROL, [Bmp180.CMD_READTEMP])
        sleep_ms(5)  # Wait 5ms

        return self._readUInt(Bmp180.REG_TEMPDATA)


    def readRawPressure(self):
        # Reads the raw (uncompensated) pressure level from the sensor
        self._write(Bmp180.REG_CONTROL, [Bmp180.CMD_READPRESSURE + (self._mode << 6)])
        if (self._mode == Bmp180.MODE_ULTRALOWPOWER):
            sleep_ms(5)
        elif (self._mode == Bmp180.MODE_HIGHRES):
            sleep_ms(14)
        elif (self._mode == Bmp180.MODE_ULTRAHIGHRES):
            sleep_ms(26)
        else:
            sleep_ms(8)
          
        msb = self._readUByte(Bmp180.REG_PRESSUREDATA)
        lsb = self._readUByte(Bmp180.REG_PRESSUREDATA +1)
        xlsb = self._readUByte(Bmp180.REG_PRESSUREDATA +2)
        
        raw = ((msb << 16) + (lsb << 8) + xlsb) >> (8 - self._mode)
        
        return raw
        

    def readTemperature(self):
        # Gets the compensated temperature in degrees celcius
        UT = 0
        X1 = 0
        X2 = 0
        B5 = 0
        temp = 0.0

        # Read raw temp before aligning it with the calibration values
        UT = self.readRawTemp()
        X1 = ((UT - self._ac6) * self._ac5) >> 15
        X2 = (self._mc << 11) // (X1 + self._md)
        B5 = X1 + X2
        temp = ((B5 + 8) >> 4 ) / 10.0
        
        return temp

    def readPressure(self):
        # Gets the compensated pressure in pascal
        UT = 0
        UP = 0
        B3 = 0
        B5 = 0
        B6 = 0
        X1 = 0
        X2 = 0
        X3 = 0
        p = 0
        B4 = 0
        B7 = 0

        UT = self.readRawTemp()
        UP = self.readRawPressure()

        # True Temperature Calculations
        X1 = ((UT - self._ac6) * self._ac5) >> 15
        X2 = (self._mc << 11) // (X1 + self._md)
        B5 = X1 + X2

        # Pressure Calculations
        B6 = B5 - 4000
        X1 = (self._b2 * (B6 * B6) >> 12) >> 11
        X2 = (self._ac2 * B6) >> 11
        X3 = X1 + X2
        B3 = (((self._ac1 * 4 + X3) << self._mode) + 2) / 4

        X1 = (self._ac3 * B6) >> 13
        X2 = (self._b1 * ((B6 * B6) >> 12)) >> 16
        X3 = ((X1 + X2) + 2) >> 2
        B4 = (self._ac4 * (X3 + 32768)) >> 15
        B7 = (UP - B3) * (50000 >> self._mode)

        if (B7 < 0x80000000):
            p = int((B7 * 2) // B4)
        else:
            p = int((B7 // B4) * 2)

        X1 = (p >> 8) * (p >> 8)
        X1 = (X1 * 3038) >> 16
        X2 = (-7375 * p) >> 16

        p = p + ((X1 + X2 + 3791) >> 4)

        return p

    def readAltitude(self, seaLevelPressure = 101325):
        # Calculates the altitude in meters
        altitude = 0.0
        pressure = float(self.readPressure())
        altitude = 44330.0 * (1.0 - pow(pressure / seaLevelPressure, 0.1903))
        
        return altitude
        
 
def main():
 
    sensor = Bmp180()
    
    print("Temp: {0} C".format(sensor.readTemperature()))
    print("Press: {0} Pa".format(sensor.readPressure()))
    print("Altitude: {0} m".format(sensor.readAltitude()))
 
if __name__ == '__main__':
    main()
 