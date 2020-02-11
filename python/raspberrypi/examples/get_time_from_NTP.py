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
import datetime
import ntplib
from DFRobot_DS3231M import *

client = ntplib.NTPClient()
response = client.request('ch.pool.ntp.org')
print(datetime.datetime.fromtimestamp(response.tx_time))

rtc = DFRobot_Sensor_IIC(1)

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
rtc.set_year(response.tx_time.year - 100)#Set year, default in the 21st century, input negative number for years in the 20th century.
rtc.set_month(response.tx_time.month)
rtc.set_date(response.tx_time.date)
'''
@brief Set the hours and 12hours or 24hours
@param hour:1-12 in 12hours,0-23 in 24hours
@param mode:e24hours, eAM, ePM
'''
rtc.set_hour(response.tx_time.hour,DS3231M_24hours)
rtc.set_minute(response.tx_time.minute)
rtc.set_second(response.tx_time.second)
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
        print("{0}/{1}/{2},{3},{4}:{5}:{6},{7}".format(rtc.year(),rtc.month(),rtc.date(),\
        rtc.day_of_the_week(),rtc.hour(),rtc.minute(),rtc.second(),rtc.get_AM_or_PM()))
        print(" ")
        time.sleep(1)

if __name__ == "__main__":
    main()
