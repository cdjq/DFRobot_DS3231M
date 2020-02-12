'''
file get_time_and_tem.py

@Through the example, you can get the time and temperature:
@Experiment phenomenon: read data every 1 seconds and print it on serial port .
@
@Copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
@licence   The MIT License (MIT)
@
@author [LuoYufeng](yufeng.luo@dfrobot.com)
@url https://github.com/DFRobot/DFRobot_DS3231M
@version  V1.0
@date  2020-2-12
'''
import sys
sys.path.append('../')
import time
from DFRobot_DS3231M import *

rtc = DFRobot_DS3231M(1)

#begin return True if succeed, otherwise return False
while not rtc.begin():
    time.sleep(2)

'''
@brief Set the vaule of pin sqw
@param mode _OFF             = 0x01 // Not output square wave, enter interrupt mode
@n          _SquareWave_1Hz  = 0x00 // 1Hz square wave
@n          _SquareWave_1kHz = 0x08 // 1kHz square wave
@n          _SquareWave_4kHz = 0x10 // 4kHz square wave
@n          _SquareWave_8kHz = 0x18 // 8kHz square wave
'''
rtc.write_sqw_pin_mode(rtc._SquareWave_1Hz)
'''
@brief Read the value of pin sqw
@return mode _OFF             = 0x01 // Off
@n           _SquareWave_1Hz  = 0x00 // 1Hz square wave
@n           _SquareWave_1kHz = 0x08 // 1kHz square wave
@n           _SquareWave_4kHz = 0x10 // 4kHz square wave
@n           _SquareWave_8kHz = 0x18 // 8kHz square wave
'''
#rtc.read_sqw_pin_mode()
'''
@brief Set the last compiled time as the current time
'''
#rtc.dateTime()#If users use this function, please don't set time by other way
rtc.set_year(20)#Set year, default in the 21st century, input negative number for years in the 20th century.
rtc.set_month(2)
rtc.set_date(11)
'''
@brief Set the hours and 12hours or 24hours
@param hour:1-12 in 12hours,0-23 in 24hours
@param mode:_24hours, _AM, _PM
'''
rtc.set_hour(12,rtc._AM)
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
        '''
        print(rtc.year()),print("/"),
        print(rtc.month()),print("/"),
        print(rtc.date()),print(","),
        print(rtc.get_day_of_the_week()),print(","),
        print(rtc.hour()),print(":"),
        print(rtc.minute()),print(":"),
        print(rtc.second()),print(","),
        print(rtc.get_AM_or_PM())
        '''
        print("{0}/{1}/{2},{3},{4}:{5}:{6},{7}".format(rtc.year(),rtc.month(),rtc.date(),\
        rtc.get_day_of_the_week(),rtc.hour(),rtc.minute(),rtc.second(),rtc.get_AM_or_PM()))
        print(temp)
        print(" ")
        time.sleep(1)

if __name__ == "__main__":
    main()

