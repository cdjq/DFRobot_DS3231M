#-*- coding: utf-8 -*-
'''
@file set_alarm_interrupt.py

@brief Through the example, you can set alarm clock in interrupt:
@n     Experiment phenomenon: read data every 1 seconds and print it on serial port .

@Copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
@licence   The MIT License (MIT)

@author [LuoYufeng](yufeng.luo@dfrobot.com)
@url https://github.com/DFRobot/DFRobot_DS3231M
@version  V1.0
@date  2020-2-12
'''
import sys
sys.path.append('../')
import time
import threading
import RPi.GPIO as GPIO
from DFRobot_DS3231M import *

rtc = DFRobot_DS3231M(bus=1)

GPIO.setmode(GPIO.BOARD)


#begin return True if succeed, otherwise return False
while not rtc.begin():
    time.sleep(2)

rtc.enable_alarm1_int();#@enable Alarm2 interrupt
'''
@brief Set the vaule of pin sqw
@param mode OFF             = 0x01 # Not output square wave, enter interrupt mode
@n          SquareWave_1Hz  = 0x00 # 1Hz square wave
@n          SquareWave_1kHz = 0x08 # 1kHz square wave
@n          SquareWave_4kHz = 0x10 # 4kHz square wave
@n          SquareWave_8kHz = 0x18 # 8kHz square wave
'''
rtc.write_sqw_pin_mode(rtc.OFF)
'''
@brief Read the value of pin sqw
@return mode OFF             = 0x01 # Off
@n           SquareWave_1Hz  = 0x00 # 1Hz square wave
@n           SquareWave_1kHz = 0x08 # 1kHz square wave
@n           SquareWave_4kHz = 0x10 # 4kHz square wave
@n           SquareWave_8kHz = 0x18 # 8kHz square wave
'''
#rtc.read_sqw_pin_mode()
'''
@brief Set the last compiled time as the current time
'''
#rtc.dateTime()#If users use this function, please don't set time by other way
rtc.set_year(19)#Set year, default in the 21st century, input negative number for years in the 20th century.
rtc.set_month(10)#Set the months in 1-12
rtc.set_date(23)#Set the dates in 0-31
'''
@brief Set the hours and 12hours or 24hours
@param hour:1-12 in 12hours,0-23 in 24hours
@param mode:H24hours, AM, PM
'''
rtc.set_hour(1,rtc.H24hours)
rtc.set_minute(59)#Set the minutes in 0-59
rtc.set_second(55)#Set the seconds in 0-59

rtc.adjust()#Set status on work
'''
@brief Set alarm clock
@param alarmType:EverySecond,
@n               SecondsMatch,
@n               SecondsMinutesMatch,
@n               SecondsMinutesHoursMatch,
@n               SecondsMinutesHoursDateMatch,
@n               SecondsMinutesHoursDayMatch, #Alarm1
@n               EveryMinute,
@n               MinutesMatch,
@n               MinutesHoursMatch,
@n               MinutesHoursDateMatch,
@n               MinutesHoursDayMatch,        #Alarm2
@n               UnknownAlarm
@param days      Alarm clock Day (day)
@param hours     Alarm clock Hour (hour)
@param mode:     H24hours, AM, PM
@param minutes   Alarm clock (minute)
@param seconds   Alarm clock (second)
'''
rtc.set_alarm(alarmType=rtc.SecondsMinutesHoursDayMatch,date=23,hour=2,mode=rtc.AM,minute=0,second=0)
'''
@brief disable the 32k output (default is enable)
'''
#rtc.disAble32k();

'''
@brief enable the 32k output 
'''
#rtc.enAble32k();

IO1 = 21#set interrupt pin

def IO1CallBack():#callback function
    global rtc
    rtc.clear_alarm()
    print("Alarm clock is triggered.")
 
GPIO.setup(IO1, GPIO.IN)
'''
@brief 当中断引脚变为高电平时，运行IO1CallBack()方法
'''
GPIO.add_event_detect(IO1, GPIO.RISING, callback = IO1CallBack)

def main():
    while True:
        #if you are a beginner of python,you can run this code
        '''
        print(rtc.get_year()),
        print("/"),
        print(rtc.get_month()),
        print("/"),
        print(rtc.get_date()),
        print(","),
        print(rtc.get_day_of_the_week()),
        print(","),
        print(rtc.get_hour()),
        print(":"),
        print(rtc.get_minute()),
        print(":"),
        print(rtc.get_second()),
        print(","),
        print(rtc.get_AM_or_PM())
        '''
        #If you have been learning Python for a while,you can run this code
        print("{0}/{1}/{2},{3},{4}:{5}:{6},{7}".format(rtc.get_year(),rtc.get_month(),rtc.get_date(),\
        rtc.get_day_of_the_week(),rtc.get_hour(),rtc.get_minute(),rtc.get_second(),rtc.get_AM_or_PM()))#print now time
        
        print(" ")
        time.sleep(1)

if __name__ == "__main__":
    main()