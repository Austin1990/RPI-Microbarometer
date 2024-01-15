#       Bonas HAT Sensor Monitoring Software
#

import os
from bmp_280 import BMP280
from sht31 import SHT31d
from sgp30 import SGP30
from time import sleep

device_0 = BMP280()
device_1 = SHT31d()
device_2 = SGP30()

os.chdir('/home/ajb/Source/Bonas_HAT')

def main():
    try:
        device_2.start_measurement()
    except IOError:
        print('SGP30 error')
    while 1:
        sleep(5)
        try:
            tempB, pressure, tempS, humidity, air_qual = read_from_sensors()
            print(f"BMP-280 Temperature : {tempB:.2f}")
            print(f"BMP-280 Pressure : {pressure:.2f}")
            print(f"SHT31 Temperature : {tempS:.2f}")
            print(f"SHT31 humidity : {humidity:.2f}\n")
            print(f"Temp diff : {(tempB-tempS):.2f}\n")
            print(f"SGP30 Equivalent CO2 : {air_qual.equivalent_co2: 5d}")
            print(f"SGP30 total VOC : {air_qual.total_voc: 5d}\n")

        except IOError:
            print('read error')


def read_from_sensors():
    # read data from BMP-280
    bmp_temp = device_0.read_temperature()
    bmp_p = device_0.read_pressure()
    # read data from SHT31
    sht_temp, sht_rh = device_1.read_temperature_humidity()
    # read data from SGP30
    air_qual = device_2.get_air_quality()
  
    readings = (bmp_temp, bmp_p, sht_temp, sht_rh, air_qual)
    return readings


if __name__ == '__main__':
    main()
