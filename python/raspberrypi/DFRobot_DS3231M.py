""" file DFRobot_DS3231M.py
  #
  # 定义DFRobot_Sensor 类的基础结构，基础方法的实现
  #
  # @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  # @licence     The MIT License (MIT)
  # @author      Alexander(ouki.wang@dfrobot.com)
  # version  V1.0
  # date  2017-10-9
  # @get from https://www.dfrobot.com
  # @url https://github.com/DFRobot/DFRobot_DS3231M
"""

import sys
sys.path.append('../')
import smbus 
from ctypes import *
import time

DS3231M_OFF                = 0x01
DS3231M_SquareWave_1Hz     = 0x00
DS3231M_SquareWave_1kHz    = 0x08
DS3231M_SquareWave_4kHz    = 0x10
DS3231M_SquareWave_8kHz    = 0x18

DS3231M_24hours            = 0
DS3231M_AM                 = 2
DS3231M_PM                 = 3

DS3231M_EverySecond                  = 0
DS3231M_SecondsMatch                 = 1
DS3231M_SecondsMinutesMatch          = 2
DS3231M_SecondsMinutesHoursMatch     = 3
DS3231M_SecondsMinutesHoursDateMatch = 4
DS3231M_SecondsMinutesHoursDayMatch  = 5

DS3231M_EveryMinute                  = 6
DS3231M_MinutesMatch                 = 7
DS3231M_MinutesHoursMatch            = 8
DS3231M_MinutesHoursDateMatch        = 9
DS3231M_MinutesHoursDayMatch         = 10

UnknownAlarm                 = 11

class DFRobot_DS3231M:
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
    _ss = 0
    _mm = 0
    _hh = 0
    _d = 0
    _m = 0
    _y = 0
    daysOfTheWeek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    hourOfAM = ["", "", "AM", "PM"] 
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
        def __init__(self, second = 0, able = 0):
            self.second = second
            self.able = able
    
    class AlarmMinute():
        _pack_ = 1
        _fields_=[('minute',c_ubyte,7),
                ('able',c_ubyte,1)]
        def __init__(self, minute = 0, able = 0):
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

    def __init__(self):
        _deviceAddr = self._IIC_ADDRESS
        
    
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
            days += pgm_read_byte(daysInMonth + i - 1)
        if (m > 2 and y % 4) == 0:
            ++days
        return days + 365 * y + (y + 3) / 4 - 1

    def conv2d(self, p):
        v = 0
        if p >= '0' and p <= '9':
            v = p - '0'
        return 10 * v + ++p - '0'


    def bcd2bin(self, val):
        return val - 6 * (val >> 4)

    def bin2bcd (self, val):
        return val + 6 * (val / 10)

    def read_sqw_pin_mode(self):
        mode = self.Control()
        mode = self.read_reg(self._REG_CONTROL)
        return mode.BBSQW

    def write_sqw_pin_mode(self, mode):
        ctrl = self.read_reg(self._REG_CONTROL)
        ctrl[0] &= 0x04
        ctrl[0] &= 0x18
        if mode == DS3231M_OFF:
            ctrl[0] |= 0x04
        else:
            ctrl[0] |= mode
        self.write_reg(self._REG_CONTROL, ctrl);
    
    def day_of_the_week(self):
        day = self.date2days(self._y, self._m, self._d)
        return (day + 6) % 7
    
    def get_day_of_the_week(self):
        return self.daysOfTheWeek[self.dayOfTheWeek()]

    def set_year(self, year):
        data = self.bin2bcd(year + 30)
        self.write_reg(self._REG_RTC_YEAR, data)
    
    def set_month(self, month):
        data = self.bin2bcd(month);
        self.write_reg(self._REG_RTC_MONTH, data)
    
    def set_date(self, date):
        data = self.bin2bcd(date)
        self.write_reg(self._REG_RTC_DATE, data);

    def set_hour(self, hour, mode):
        if mode == 0:
            data = self.Now24Hour()
            data.hour = self.bin2bcd(hour)
            data.mode = mode
            self.write_reg(self._REG_RTC_HOUR, data)
        else:
            data = self.Now12Hour()
            data.hour = bin2bcd(hour)
            data.mode = mode
            self.write_reg(self._REG_RTC_HOUR, data)
    
    def set_minute(self,minute):
        data = self.bin2bcd(minute)
        self.write_reg(self._REG_RTC_MIN, data)
    
    def set_second(self, second):
        data = self.bin2bcd(second)
        self.write_reg(self._REG_RTC_SEC, data)
    
    def get_AM_or_PM(self):
        buffer = self.read_reg(self._REG_RTC_HOUR)
        buffer[0] = buffer[0] << 1
        buffer[0] = buffer[0] >> 6
        return self.hourOfAM[buffer[0]]
        
    def adjust(self):
        statreg = self.read_reg(self._REG_STATUS)
        statreg[0] &= ~0x80
        self.write_reg(self._REG_STATUS, statreg)
    
    def get_now_time(self):
        self.bcd = self.read_reg(self._REG_RTC_SEC)
        self._ss = self.bcd2bin(self.bcd[0] & 0x7F)
        self._mm = self.bcd2bin(self.bcd[1])
        self.bcd[2] = self.bcd[2] << 3
        self._hh = self.bcd2bin(self.bcd[2] >> 3)
        self._d = self.bcd2bin(self.bcd[4])
        self._m = self.bcd2bin(self.bcd[5])
        self._y = self.bcd2bin(self.bcd[6]) + 1970
        if(self.bcd[5] > 80):
            self._y += 100
            self._m -= 80
    
    def year(self):
        return self._y
    
    def month(self):
        return self._m
    
    def date(self):
        return self._d
    
    def hour(self):
        return self._hh
    
    def minute(self):
        return self._mm
    
    def second(self):
        return self._ss
    
    def get_temperature_C(self):
        buf = self.read_reg(self._REG_TEMPERATURE)
        return (buf[0] + (buf[1]>>6)*0.25)
    
    def lost_power(self):
        status = self.read_reg(DS3231M_REG_STATUS)
        return status[0] >> 7
    
    def set_alarm(self, alarmType, date, hour, mode, minute, second, state ):
        conReg = self.Control()
        conReg = self.read_reg(_REG_CONTROL)
        dates = AlarmDate()
        hours = AlarmxxHour()
        if mode == 0:
            hours24 = Alarm24Hour()
            hours.hour = hours24.hour
            hours.mode = hours24.mode
            hours.able = hours24.able
        else:
            hours12 = Alarm12Hour()
            hours.hour = hours12.hour
            hours.mode = hours12.mode
            hours.able = hours12.able
        minutes = AlarmMinute()
        seconds = AlarmSecond()
        if alarmType >= UnknownAlarm:
            return
        if alarmType < EveryMinute:
            self.write_reg(self._REG_ALM1_SEC, seconds)
            self.write_reg(self._REG_ALM1_MIN, minutes)
            self.write_reg(self._REG_ALM1_HOUR, hours)
            if alarmType == SecondsMinutesHoursDateMatch:
                self.write_reg(self._REG_ALM1_DAY, dates)
            else:
                self.write_reg(self._REG_ALM1_DAY, days);
            if alarmType < SecondsMinutesHoursDateMatch:
                dates.able = 1
            if alarmType < SecondsMinutesHoursMatch:
                hours.able = 1
            if alarmType < SecondsMinutesMatch:
                minutes.able = 1
            if alarmType == eEverySecond:
                seconds.able = 1
            if alarmType == eSecondsMinutesHoursDayMatch:
                dates.dayOrDate = 1
            if state == True:
                conReg.A1IE = 0
            else:
                conReg.A1IE = 0
        else:
            if alarmType == MinutesHoursDateMatch:
                self.write_reg(self._DS3231M_REG_ALM2_DAY, dates)
            elif alarmType == eMinutesHoursDayMatch:
                days[0] |= 0x80
                self.write_reg(self._DS3231M_REG_ALM2_DAY)
            if alarmType < MinutesHoursDateMatch:
                dates.able = 1
            if alarmType < MinutesHoursMatch:
                hours.able = 1
            if alarmType == EveryMinute:
                minutes.able = 1
            if state == True:
                conReg.A2IE = 1;
            else:
                conReg.A2IE = 0;
            self.write_reg(self._DS3231M_REG_ALM2_MIN, minutes);
            self.write_reg(self._DS3231M_REG_ALM2_HOUR, hours);
        self.clear_alarm()
        return
    
    def enable_alarm1_int(self):
        conReg = self.Control()
        conReg = self.read_reg(self._REG_CONTROL)
        conReg.A1IE = 1
        self.write_reg(self._REG_CONTROL, conReg)
    
    def disable_alarm1_int(self):
        conReg = self.Control()
        conReg = self.read_reg(self._REG_CONTROL)
        conReg.A1IE = 0
        self.write_reg(self._REG_CONTROL, conReg)
    
    def enable_alarm2_int(self):
        conReg = self.Control()
        conReg = self.read_reg(self._REG_CONTROL)
        conReg.A2IE = 1
        self.write_reg(self._REG_CONTROL, conReg)
    
    def disable_alarm2_int(self):
        conReg = self.Control()
        conReg = self.read_reg(self._REG_CONTROL)
        conReg.A2IE = 0
        self.write_reg(self._REG_CONTROL, conReg)
    
    def is_alarm(self):
        staReg = self.Status()
        staReg = self.read_reg(self._REG_STATUS)
        return staReg.A1F & staReg.A2F 
    
    def clear_alarm(self):
        staReg = self.Status()
        staReg = self.read_reg(self._REG_STATUS)
        staReg.A1F = 0;
        staReg.A2F = 0;
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


class DFRobot_Sensor_IIC(DFRobot_DS3231M):
    def __init__(self, bus, mode):
        self.i2cbus=smbus.SMBus(bus)
        self.i2c_addr = DFRobot_DS3231M._IIC_ADDRESS
        super().__init__()

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
