'''
file set_alarm_in_query.py

@Through the example, you can set alarm clock in query:
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
@param mode eDS3231M_OFF             = 0x01 // Not output square wave, enter interrupt mode
@n          eDS3231M_SquareWave_1Hz  = 0x00 // 1Hz square wave
@n          eDS3231M_SquareWave_1kHz = 0x08 // 1kHz square wave
@n          eDS3231M_SquareWave_4kHz = 0x10 // 4kHz square wave
@n          eDS3231M_SquareWave_8kHz = 0x18 // 8kHz square wave
'''
rtc.write_sqw_pin_mode(rtc._SquareWave_1Hz)
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
@param mode:_24hours,_AM,_PM
'''
rtc.set_hour(0,rtc._24hours)
rtc.set_minute(59)
rtc.set_second(40)

rtc.adjust()
'''
@brief Set alarm clock
@param alarmType Alarm clock working mode:
@n _EverySecond,
@n _SecondsMatch,
@n _SecondsMinutesMatch,
@n _SecondsMinutesHoursMatch,
@n _SecondsMinutesHoursDateMatch,
@n _SecondsMinutesHoursDayMatch, //Alarm1
@n _EveryMinute,
@n _MinutesMatch,
@n _MinutesHoursMatch,
@n _MinutesHoursDateMatch,
@n _MinutesHoursDayMatch,        //Alarm2
@n _UnknownAlarm
@param days    Alarm clock Day (day)
@param hours   Alarm clock Hour (hour)
@param mode:   _24hours, _AM, _PM
@param minutes Alarm clock (minute)
@param seconds Alarm clock (second)
'''
rtc.set_alarm(alarmType=rtc._SecondsMatch,date=27,hour=12,mode=rtc._AM,minute=0,second=0)
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
        if rtc.isAlarm() == True:
            print("Alarm clock is triggered.")
            rtc.clearAlarm()
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
        print(" ")
        time.sleep(1)

if __name__ == "__main__":
    main()