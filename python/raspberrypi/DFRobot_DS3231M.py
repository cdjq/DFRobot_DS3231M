""" 
@file DFRobot_DS3231M.py

@brief Define the basic structure of class DFRobot_DS3231M

@copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
@licence     The MIT License (MIT)
@author [LuoYufeng](yufeng.luo@dfrobot.com)
@version  V1.0
@date  2020-2-12
@get from https://www.dfrobot.com
@url https://github.com/DFRobot/DFRobot_DS3231M
"""

import sys
sys.path.append('../')
import smbus 
from ctypes import *
import time


class DFRobot_DS3231M:
    
    OFF                = 0x01
    SquareWave_1Hz     = 0x00
    SquareWave_1kHz    = 0x08
    SquareWave_4kHz    = 0x10
    SquareWave_8kHz    = 0x18
    
    H24hours            = 0
    AM                 = 2
    PM                 = 3
    
    EverySecond                  = 0
    SecondsMatch                 = 1
    SecondsMinutesMatch          = 2
    SecondsMinutesHoursMatch     = 3
    SecondsMinutesHoursDateMatch = 4
    SecondsMinutesHoursDayMatch  = 5
    
    EveryMinute                  = 6
    MinutesMatch                 = 7
    MinutesHoursMatch            = 8
    MinutesHoursDateMatch        = 9
    MinutesHoursDayMatch         = 10

    UnknownAlarm                 = 11

    _IIC_ADDRESS        = 0x68

    _SECONDS_FROM_1970_TO_2000  = 946684800
    _REG_RTC_SEC        = 0X00
    _REG_RTC_MIN        = 0X01
    _REG_RTC_HOUR       = 0X02
    _REG_RTC_DAY        = 0X03
    _REG_RTC_DATE       = 0X04
    _REG_RTC_MONTH      = 0X05
    _REG_RTC_YEAR       = 0X06
    _REG_ALM1_SEC       = 0X07
    _REG_ALM1_MIN       = 0X08
    _REG_ALM1_HOUR      = 0X09
    _REG_ALM1_DAY       = 0X0A
    _REG_ALM2_MIN       = 0X0B
    _REG_ALM2_HOUR      = 0X0C
    _REG_ALM2_DAY       = 0X0D
    _REG_CONTROL        = 0x0E
    _REG_STATUS         = 0x0F
    _REG_AGE_OFFSET     = 0X10
    _REG_TEMPERATURE    = 0x11
    
    rtc_bcd = []
    bcd = []
    _d = 0
    _m = 0
    _y = 0
    ss = 0
    mm = 0
    hh = 0
    d = 0
    m = 0
    y = 0
    days_in_month = [31,28,31,30,31,30,31,31,30,31,30,31]
    days_of_the_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    hour_of_am = [" ", " ", "AM", "PM"] 
    '''
    class NowTime():
        def __init__(self, year, month, date, hour, minute, second):
            self._y = year
            self._m = month
            self._d = date
            self._hh = hour
            self._mm = minute
            self._ss = second
    '''
    class Now24Hour():
        _pack_ = 1
        _fields_=[('hour',c_ubyte,6),
                ('mode',c_ubyte,2)]
        def __init__(self, hour = 0, mode = 1):
            self.hour = hour
            self.mode = mode

    class Now12Hour():
        _pack_ = 1
        _fields_=[('hour',c_ubyte,5),
                ('mode',c_ubyte,3)]
        def __init__(self, hour = 0, mode = 1):
            self.hour = hour
            self.mode = mode
    
    class NowMonth():
        _pack_ = 1
        _fields_=[('century',c_ubyte,1),
                ('month',c_ubyte,7)]
        def __init__(self, century = 0, month = 0):
            self.century = century
            self.month = month
    
    class AlarmSecond():
        _pack_ = 1
        _fields_=[('second',c_ubyte,7),
                ('able',c_ubyte,1)]
        def __init__(self, second, able = 0):
            self.second = second
            self.able = able
    
    class AlarmMinute():
        _pack_ = 1
        _fields_=[('minute',c_ubyte,7),
                ('able',c_ubyte,1)]
        def __init__(self, minute, able = 0):
            self.minute = minute
            self.able = able
    
    class Alarm24Hour():
        _pack_ = 1
        _fields_=[('hour',c_ubyte,6),
                ('mode',c_ubyte,1),
                ('able',c_ubyte,1)]
        def __init__(self, hour, mode = 0, able = 0):
            self.hour = hour
            self.mode = mode
            self.able = able
    
    class Alarm12Hour():
        _pack_ = 1
        _fields_=[('hour',c_ubyte,5),
                ('mode',c_ubyte,2),
                ('able',c_ubyte,1)]
        def __init__(self, hour, mode = 0, able = 0):
            self.hour = hour
            self.mode = mode
            self.able = able
    
    class AlarmxxHour():
        _pack_ = 1
        _fields_=[('hour'),
                ('mode'),
                ('able')]
        def __init__(self, hour, mode = 0, able = 0):
            self.hour = hour
            self.mode = mode
            self.able = able
    
    
    class AlarmDate():
        _pack_ = 1
        _fields_=[('date',c_ubyte,6),
                ('dayOrDate',c_ubyte,1),
                ('able',c_ubyte,1)]
        def __init__(self, date, dayOrDate = 0, able = 0):
            self.date = date
            self.dayOrDate = dayOrDate
            self.able = able

    class Control():
        _pack_ = 1
        _fields_=[('A1IE',c_ubyte,1),
                ('A2IE',c_ubyte,1),
                ('INTCN',c_ubyte,3),
                ('CONV',c_ubyte,1),
                ('BBSQW',c_ubyte,1),
                ('EOSC',c_ubyte,1)]
        def __init__(self, EOSC = 1, BBSQW = 1, CONV = 1, INTCN = 1, A2IE = 1, A1IE = 1):
            self.A1IE = A1IE
            self.A2IE = A2IE
            self.INTCN = INTCN
            self.CONV = CONV
            self.BBSQW = BBSQW
            self.EOSC = EOSC


    class Status():
        _pack_ = 1
        _fields_=[('A1F',c_ubyte,1),
                ('A2F',c_ubyte,1),
                ('BSY ',c_ubyte,1),
                ('EN32KHZ',c_ubyte,1),
                ('OSF',c_ubyte,4)]
        def __init__(self, A1F = 0, A2F = 0, BSY = 0, EN32KHZ = 0, OSF = 0):
            self.A1F = A1F
            self.A2F = A2F
            self.BSY = BSY
            self.EN32KHZ = EN32KHZ
            self.OSF = OSF

    def __init__(self, bus):
        _deviceAddr = self._IIC_ADDRESS
        self.i2cbus=smbus.SMBus(bus)
        self.i2c_addr = self._IIC_ADDRESS
    
    def begin(self):
        if not self.scan():
            return False
        else:
            return True

    def date2days(self, y, m, d):
        if y >= 2000:
            y -= 2000
        days = d
        for i in range(1, m):
            days += self.days_in_month[i - 1]
        if (m > 2 and y % 4) == 0:
            ++days
        return days + 365 * y + int((y + 3) / 4) - 1

    def conv2d(self, p):
        v = 0
        if p >= '0' and p <= '9':
            v = p - '0'
        return 10 * v + ++p - '0'


    def bcd2bin(self, val):
        return val - 6 * (val >> 4)

    def bin2bcd (self, val):
        return val + 6 * int(val / 10)

    def read_sqw_pin_mode(self):
        mode = self.Control()
        mode = self.read_reg(self._REG_CONTROL)
        return mode.BBSQW

    def write_sqw_pin_mode(self, mode):
        ctrl = self.read_reg(self._REG_CONTROL)
        ctrl[0] &= 0x04
        ctrl[0] &= 0x18
        if mode == self.OFF:
            ctrl[0] |= 0x04
        else:
            ctrl[0] |= mode
        self.write_reg(self._REG_CONTROL, ctrl);
    
    def day_of_the_week(self):
        day = self.date2days(self._y, self._m, self._d)
        return (day + 6) % 7
    
    def get_day_of_the_week(self):
        return self.days_of_the_week[self.day_of_the_week()]

    def set_year(self, year):
        self.y = self.bin2bcd(year + 30)
    
    def set_month(self, month):
        self.m = self.bin2bcd(month)
    
    def set_date(self, date):
        self.d = self.bin2bcd(date)

    def set_hour(self, hour, mode):
        if mode == 0:
            self.hh = self.bin2bcd(hour) | (mode << 6)
        else:
            self.hh = self.bin2bcd(hour) | (mode << 5)
    
    def set_minute(self,minute):
        self.mm = self.bin2bcd(minute)
    
    def set_second(self, second):
        self.ss = self.bin2bcd(second)
    
    def get_AM_or_PM(self):
        buffer = self.read_reg(self._REG_RTC_HOUR)
        buffer[0] = buffer[0] & 0x60
        buffer[0] = buffer[0] >> 5
        return self.hour_of_am[buffer[0]]
        
    def adjust(self):
        data = [self.ss, self.mm, self.hh, self.day_of_the_week(), self.d, self.m, self.y]
        self.write_reg(self._REG_RTC_SEC, data)
        statreg = self.read_reg(self._REG_STATUS)
        statreg[0] &= ~0x80
        self.write_reg(self._REG_STATUS, statreg)
    
    def get_year(self):
        year = self.read_reg(self._REG_RTC_YEAR)
        self._y = self.bcd2bin(year[0]) + 1970
        century = self.read_reg(self._REG_RTC_MONTH)
        if century[0] > 80:
            self._y += 100
        return self._y
    
    def get_month(self):
        month = self.read_reg(self._REG_RTC_MONTH)
        self._m = self.bcd2bin(month[0])
        if self._m > 80:
            self._m -= 80
        return self._m
    
    def get_date(self):
        date = self.read_reg(self._REG_RTC_DATE)
        self._d = self.bcd2bin(date[0])
        return self._d 
    
    def get_hour(self):
        hour = self.read_reg(self._REG_RTC_HOUR)
        self._hh = self.bcd2bin(hour[0] & 0x1F)
        #self._hh = self._hh >> 3
        return self._hh
    
    def get_minute(self):
        minute = self.read_reg(self._REG_RTC_MIN)
        self._mm = self.bcd2bin(minute[0])
        return self._mm
    
    def get_second(self):
        second = self.read_reg(self._REG_RTC_SEC)
        self._ss = self.bcd2bin(second[0] & 0x7F)
        return self._ss
    
    def get_temperature_C(self):
        buf = self.read_reg(self._REG_TEMPERATURE)
        return (buf[0] + (buf[1]>>6)*0.25)
    
    def get_temperature_F(self):
        buf = self.read_reg(self._REG_TEMPERATURE)
        c = (buf[0] + (buf[1]>>6)*0.25)
        return c * 9 / 5 + 32
    
    def is_lost_power(self):
        status = self.read_reg(DS3231M_REG_STATUS)
        return status[0] >> 7
    
    def set_alarm(self, alarmType, date, hour, mode, minute, second, state = True):
        dates = [self.bin2bcd(date)]
        hours = [mode >> 6|self.bin2bcd(hour)]
        minutes = [self.bin2bcd(minute)]
        seconds = [self.bin2bcd(second)]
        days = [self.bin2bcd(self.day_of_the_week())]
        buffer = []
        if alarmType >= self.UnknownAlarm:
            return
        if alarmType < self.EveryMinute:
            self.write_reg(self._REG_ALM1_SEC, seconds)
            self.write_reg(self._REG_ALM1_MIN, minutes)
            self.write_reg(self._REG_ALM1_HOUR, hours)
            if alarmType == self.SecondsMinutesHoursDateMatch:
                self.write_reg(self._REG_ALM1_DAY, dates)
            else:
                self.write_reg(self._REG_ALM1_DAY, days);
            if alarmType < self.SecondsMinutesHoursDateMatch:
                buffer = self.read_reg(self._REG_ALM1_DAY)
                buffer[0] |= 0x80
                self.write_reg(self._REG_ALM1_DAY, buffer)
            if alarmType < self.SecondsMinutesHoursMatch:
                buffer = self.read_reg(self._REG_ALM1_HOUR)
                buffer[0] |= 0x80
                self.write_reg(self._REG_ALM1_HOUR, buffer)
            if alarmType < self.SecondsMinutesMatch:
                buffer = self.read_reg(self._REG_ALM1_MIN)
                buffer[0] |= 0x80
                self.write_reg(self._REG_ALM1_MIN, buffer)
            if(alarmType == self.EverySecond):
                buffer = self.read_reg(self._REG_ALM1_SEC)
                buffer[0] |= 0x80
                self.write_reg(self._REG_ALM1_SEC, buffer)
            if(alarmType == self.SecondsMinutesHoursDayMatch):
                buffer = self.read_reg(self._REG_ALM1_DAY)
                buffer[0] |= 0x40
                self.write_reg(self._REG_ALM1_DAY, buffer)
            if state == True:
                buffer = self.read_reg(self._REG_CONTROL)
                buffer[0] |= 1
                self.write_reg(self._REG_CONTROL, buffer)
            else:
                buffer = self.read_reg(self._REG_CONTROL)
                buffer[0] &= 0xFE
                self.write_reg(self._REG_CONTROL, buffer)
        else:
            self.write_reg(self._REG_ALM2_MIN, minutes)
            self.write_reg(self._REG_ALM2_HOUR, hours)
            if alarmType == self.MinutesHoursDateMatch:
                self.write_reg(self._DS3231M_REG_ALM2_DAY)
            elif alarmType == self.MinutesHoursDayMatch:
                days[0] |= 0x80
                self.write_reg(self._REG_ALM2_DAY, days)
            if alarmType < self.MinutesHoursDateMatch:
                buffer = self.read_reg(self._REG_ALM2_DAY)
                buffer[0] |= 0x80;
                self.write_reg(self._REG_ALM2_DAY, buffer)
            if alarmType < self.MinutesHoursMatch:
                buffer = self.read_reg(self._REG_ALM2_HOUR)
                buffer[0] |= 0x80
                self.write_reg(self._REG_ALM2_HOUR, buffer)
            if alarmType == self.EveryMinute:
                buffer = self.read_reg(self._REG_ALM2_MIN,)
                buffer[0] |= 0x80
                self.write_reg(self._REG_ALM2_MIN, buffer)
            if state == True:
                buffer = self.read_reg(self._REG_CONTROL)
                buffer[0] |= 2
                self.write_reg(self._REG_CONTROL, buffer)
            else:
                buffer = self.read_reg(self._REG_CONTROL)
                buffer[0] &= 0xFD
                self.write_reg(self._REG_CONTROL, buffer)
        buf = self.read_reg(self._REG_ALM1_MIN)
        print(buf[0])
        self.clear_alarm()
        return
    
    def enable_alarm1_int(self):
        conReg = self.read_reg(self._REG_CONTROL)
        conReg[0] |= 0x01
        self.write_reg(self._REG_CONTROL, conReg)
    
    def disable_alarm1_int(self):
        conReg = self.read_reg(self._REG_CONTROL)
        conReg[0] &= 0xFE
        self.write_reg(self._REG_CONTROL, conReg)
    
    def enable_alarm2_int(self):
        conReg = self.read_reg(self._REG_CONTROL)
        conReg[0] |= 0x02
        self.write_reg(self._REG_CONTROL, conReg)
    
    def disable_alarm2_int(self):
        conReg = self.read_reg(self._REG_CONTROL)
        conReg[0] &= 0xFD
        self.write_reg(self._REG_CONTROL, conReg)
    
    def is_alarm(self):
        staReg = self.read_reg(self._REG_STATUS)
        return staReg[0]&3
    
    def clear_alarm(self):
        staReg = self.read_reg(self._REG_STATUS)
        staReg[0] &= 0xFC
        self.write_reg(self._REG_STATUS, staReg)
    
    def enable_32k(self):
        staReg = self.Status()
        staReg = self.read_reg(self._REG_STATUS)
        staReg.en32kHZ = 1
        self.write_reg(self._REG_STATUS, staReg)
    
    def disable_32k(self):
        staReg = self.Status()
        staReg = self.read_reg(self._REG_STATUS)
        staReg.en32kHZ = 0
        self.write_reg(self._REG_STATUS, staReg)

    def write_reg(self, reg, buff):
        self.i2cbus.write_i2c_block_data(self.i2c_addr, reg, buff)

    def read_reg(self, reg):
        return self.i2cbus.read_i2c_block_data(self.i2c_addr, reg) 

    def scan(self):
        try:
            self.i2cbus.read_byte(self.i2c_addr)
            return True
        except:
            print("I2C init fail")
            return False
