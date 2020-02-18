#-*- coding: utf-8 -*-
'''
@file get_time_from_NTP.py

@brief Through the example, you can get the accurate time from NTP server:
@n     Experiment phenomenon: read data every 1 seconds and print it on terminal .

@Copyright Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
@licence   The MIT License (MIT)

@author [LuoYufeng](yufeng.luo@dfrobot.com)
@url https://github.com/DFRobot/DFRobot_DS3231M
@version  V1.0
@date  2020-2-12
'''
import sys
sys.path.append('../')
import time
import datetime
import ntplib
from DFRobot_DS3231M import *

rtc = DFRobot_DS3231M(bus=1)

#begin return True if succeed, otherwise return False
while not rtc.begin():
    time.sleep(2)

'''
@brief Set the vaule of pin sqw
@param mode OFF             = 0x01 # Not output square wave, enter interrupt mode
@n          SquareWave_1Hz  = 0x00 # 1Hz square wave
@n          SquareWave_1kHz = 0x08 # 1kHz square wave
@n          SquareWave_4kHz = 0x10 # 4kHz square wave
@n          SquareWave_8kHz = 0x18 # 8kHz square wave
'''
rtc.write_sqw_pin_mode(rtc.SquareWave_1Hz)
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
get the NTP time as the current time
'''
client = ntplib.NTPClient()
response = client.request('ch.pool.ntp.org')

rtc.set_year(response.tx_time.year - 100)#Set year from NTP server
rtc.set_month(response.tx_time.month)#Set the months from NTP server
rtc.set_date(response.tx_time.date)#Set the dates from NTP server
rtc.set_hour(response.tx_time.hour,rtc.H24hours)#Set the hours from NTP server
rtc.set_minute(response.tx_time.minute)#Set the minutes from NTP server
rtc.set_second(response.tx_time.second)#Set the seconds from NTP server
rtc.adjust()#Set status on work

print("Get NTP time from 'ch.pool.ntp.org' is")
print(datetime.datetime.fromtimestamp(response.tx_time))#print now time from NTP server
print("Now this time has been input to DS3231M")

#rtc.disAble32k();#disable the 32k output (default is enable)

#rtc.enAble32k();#enable the 32k output 

def main():
    while True:
        #如果您不是很熟悉python，可以这样打印
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
        #5.如果您很熟悉python，可以这样打印数据
        print("{0}/{1}/{2},{3},{4}:{5}:{6},{7}".format(rtc.get_year(),rtc.get_month(),rtc.get_date(),\
        rtc.get_day_of_the_week(),rtc.get_hour(),rtc.get_minute(),rtc.get_second(),rtc.get_AM_or_PM()))#print now time
        print(" ")
        time.sleep(1)

if __name__ == "__main__":
    main()
