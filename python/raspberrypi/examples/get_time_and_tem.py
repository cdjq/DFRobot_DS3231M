'''
file read_all_data.py

Through the example, you can get the sensor data by using getSensorData:
get all data of magnetometer, gyroscope, accelerometer.

With the rotation of the sensor, data changes are visible.

Copyright   [DFRobot](http://www.dfrobot.com), 2016
Copyright   GNU Lesser General Public License

version  V1.0
date  2019-7-9
'''
import sys
sys.path.append('../')
import time
from DFRobot_DS3231M import *

rtc = DFRobot_Sensor_IIC(0,DFRobot_Sensor_IIC)

#begin return True if succeed, otherwise return False
while not rtc.begin():
    time.sleep(2)

'''
@brief Set the vaule of pin sqw
@param mode eDS3231M_OFF             = 0x01 // Not output square wave, enter interrupt mode
@n          eDS3231M_SquareWave_1Hz  = 0x00 // 1Hz square wave
@n          eDS3231M_SquareWave_1kHz = 0x08 // 1kHz square wave
@n          eDS3231M_SquareWave_4kHz = 0x10 // 4kHz square wave
@n          eDS3231M_SquareWave_8kHz = 0x18 // 8kHz square wave
'''
rtc.write_sqw_pin_mode(DS3231M_SquareWave_1Hz)
'''
@brief Read the value of pin sqw
@return mode DS3231M_OFF             = 0x01 // Off
@n           DS3231M_SquareWave_1Hz  = 0x00 // 1Hz square wave
@n           DS3231M_SquareWave_1kHz = 0x08 // 1kHz square wave
@n           DS3231M_SquareWave_4kHz = 0x10 // 4kHz square wave
@n           DS3231M_SquareWave_8kHz = 0x18 // 8kHz square wave
'''
#rtc.read_sqw_pin_mode()
'''
@brief Set the last compiled time as the current time
'''
#rtc.dateTime()#If users use this function, please don't set time by other way
rtc.set_year(19)#Set year, default in the 21st century, input negative number for years in the 20th century.
rtc.set_month(10)
rtc.set_date(23)
'''
@brief Set the hours and 12hours or 24hours
@param hour:1-12 in 12hours,0-23 in 24hours
@param mode:e24hours, eAM, ePM
'''
rtc.set_hour(0,DS3231M_24hours)
rtc.set_minute(59)
rtc.set_second(40)

rtc.adjust()

'''
@brief enable the 32k output (default is enable)
'''
#rtc.disAble32k();

'''
@brief disable the 32k output 
'''
#rtc.enAble32k();

def main():
    while True:
        data = rtc.get_now_time()
        temp = rtc.get_temperature_C()
        print("{0:.2f}/{1:.2f}/{2:.2f},{3:.2f},{4:.2f}:{5:.2f}:{6:.2f},{7:.2f}".format(rtc.year(),\
        rtc.month(),rtc.date(),rtc.day_of_the_week(),rtc.hour(),rtc.minute(),rtc.second(),rtc.get_AM_or_PM()))
        print(temp)
        print(" ")
        time.sleep(1)

if __name__ == "__main__":
    main()

