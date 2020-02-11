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
import threading
from gpio import GPIO
from DFRobot_DS3231M import *

rtc = DFRobot_Sensor_IIC(1)
IRQ_PIN = 7

GPIO.setmode(GPIO.BOARD)

#begin return True if succeed, otherwise return False
while not rtc.begin():
    time.sleep(2)

'''
@brief enable Alarm2 interrupt
'''
rtc.enable_alarm1_int();
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

rtc.set_alarm(DS3231M_SecondsMatch,27,'''hour,1-12 in 12hours,0-23 in 24hours'''12,DS3231M_AM,'''minute,0-59'''0,'''second,0-59'''0)
'''
@brief enable the 32k output (default is enable)
'''
#rtc.disAble32k();

'''
@brief disable the 32k output 
'''
#rtc.enAble32k();

IO1 = 21
IO1Lock = threading.Lock()
IO1Flag = False

def IO1CallBack():
  global IO1Lock, IO1Flag
  IO1Lock.acquire() # wait key A lock release
  IO1Flag = True
  IO1Lock.release()
 
io1 = GPIO(IO1, GPIO.IN)
io1.setInterrupt(GPIO.RISING, IO1CallBack)

def main():
    while True:
        global IO1Lock, IO1Flag
        data = rtc.get_now_time()
        while IO1Flag:
            IO1Lock.acquire() # wait io1 release
            IO1Flag = False
            IO1Lock.release()
            print("Alarm clock is triggered.")
            rtc.clearAlarm()
        print("{0}/{1}/{2},{3},{4}:{5}:{6},{7}".format(rtc.year(),rtc.month(),rtc.date(),\
        rtc.day_of_the_week(),rtc.hour(),rtc.minute(),rtc.second(),rtc.get_AM_or_PM()))
        print(temp)
        print(" ")
        time.sleep(1)

if __name__ == "__main__":
    main()