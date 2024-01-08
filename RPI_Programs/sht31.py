from smbus2 import SMBus
from time import sleep

class SHT31d:
    SHT31_ADDR = 0x44
    
    MEASURE_SS_CSE = 0x2C
    MEASURE_SS_CSD = 0x24
    HEATER = 0x30

    HIGH_SS_CSE = 0x06
    MEDIUM_SS_CSE = 0x0D
    LOW_SS_CSE = 0x10
    HIGH_SS_CSD = 0x00
    MEDIUM_SS_CSD = 0x0B
    LOW_SS_CSD = 0x16
    
    HEATER_ON = 0x6D
    HEATER_OFF = 0x66
    
    STATUS_REG1 = 0xF3
    STATUS_REG2 = 0x2D
    
    STATUS_CLEAR_REG1 = 0x30
    STATUS_CLEAR_REG2 = 0x41
    
    CELSIUS = 0x00
    FAHRENHEIT = 0x01
    
    def __init__(self, port=1):
        self.bus = SMBus(port)

    def read_temperature_humidity(self, scale=CELSIUS):
        # SHT31 address, 0x44(68)
        # Send measurement command, 0x2C(44)
        # High repeatability measurement, 0x06(06)
        self.bus.write_i2c_block_data(self.SHT31_ADDR, self.MEASURE_SS_CSE, [self.HIGH_SS_CSE])
        
        sleep(0.015)
        
        # SHT31 address, 0x44(68)
        # Read data back from 0x00(00), 6 bytes
        # Temp_MSB, Temp_LSB, Temp_CRC, Humididty_MSB, Humidity_LSB, Humidity_CRC
        rawData = self.bus.read_i2c_block_data(self.SHT31_ADDR, 0x00, 6)
        
        # validate the temperature data
        if rawData[2] != self._crc8(rawData[0:2]):
            return (float("nan"), float("nan"))

        rawTemperature = rawData[0] << 8 | rawData[1]
        
        if (scale == self.CELSIUS):
            temperatureC = -45.0 + 175.0 * (rawTemperature / 0xFFFF)    # Celsius conversion
        else:
            temperatureF = -49.0 + 315.0 * (rawTemperature / 0xFFFF)    # Fahrenheit conversion

        # validate the humidity data
        if rawData[5] != self._crc8(rawData[3:5]):
            return (float("nan"), float("nan"))

        rawHumidity = rawData[3] << 8 | rawData[4]
        humidity = 100.0 * (rawHumidity / 0xFFFF)

        return temperatureC, humidity

    def heater_on(self):
        self.bus.write_i2c_block_data(self.SHT31_ADDR, self.HEATER, [self.HEATER_ON])

    def heater_off(self):
        self.bus.write_i2c_block_data(self.SHT31_ADDR, self.HEATER, [self.HEATER_OFF])

    def read_status(self):
        self.bus.write_i2c_block_data(self.SHT31_ADDR, self.STATUS_REG1, [self.STATUS_REG2])
        rawStatus = self.bus.read_i2c_block_data(self.SHT31_ADDR, 0x00, 3)
        if rawStatus[2] != self._crc8(rawStatus):
            return (float("nan"))
        status = rawStatus[0] << 8 | rawStatus[1]

        return status
  
    def clear_status(self):
        self.bus.write_i2c_block_data(self.SHT31_ADDR, self.STATUS_CLEAR_REG1, [self.STATUS_CLEAR_REG2])

    def _crc8(self, buffer):
        """ Polynomial 0x31 (x8 + x5 + x4 + 1) """

        polynomial = 0x31;
        crc = 0xFF;
  
        index = 0
        for index in range(0, len(buffer)):
            crc ^= buffer[index]
            for i in range(8, 0, -1):
                if crc & 0x80:
                    crc = (crc << 1) ^ polynomial
                else:
                    crc = (crc << 1)
        return crc & 0xFF