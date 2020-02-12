'''
file get_time_from_NTP.py

@Through the example, you can get the accurate time from NTP server:
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
import datetime
import ntplib
from DFRobot_DS3231M import *

rtc = DFRobot_DS3231M(1)

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

rtc.set_year(response.tx_time.year - 100)#Set year, default in the 21st century, input negative number for years in the 20th century.
rtc.set_month(response.tx_time.month)
rtc.set_date(response.tx_time.date)
rtc.set_hour(response.tx_time.hour,rtc.H24hours)
rtc.set_minute(response.tx_time.minute)
rtc.set_second(response.tx_time.second)
rtc.adjust()

print(datetime.datetime.fromtimestamp(response.tx_time))

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
        '''
        print(rtc.year()),
        print("/"),
        print(rtc.month()),
        print("/"),
        print(rtc.date()),
        print(","),
        print(rtc.get_day_of_the_week()),
        print(","),
        print(rtc.hour()),
        print(":"),
        print(rtc.minute()),
        print(":"),
        print(rtc.second()),
        print(","),
        print(rtc.get_AM_or_PM())
        '''
        print("{0}/{1}/{2},{3},{4}:{5}:{6},{7}".format(rtc.year(),rtc.month(),rtc.date(),\
        rtc.get_day_of_the_week(),rtc.hour(),rtc.minute(),rtc.second(),rtc.get_AM_or_PM()))
        print(" ")
        time.sleep(1)

if __name__ == "__main__":
    main()
