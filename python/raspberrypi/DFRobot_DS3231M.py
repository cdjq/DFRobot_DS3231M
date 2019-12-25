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
import time

DS3231M_OFF                = 0x01
DS3231M_SquareWave_1Hz     = 0x00
DS3231M_SquareWave_1kHz    = 0x08
DS3231M_SquareWave_4kHz    = 0x10
DS3231M_SquareWave_8kHz    = 0x18

24hours                    = 0
AM                         = 2
PM                         = 3

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

class DFRobot_DS3231M:
    _DS3231M_IIC_ADDRESS        = 0x68
                                =
    _SECONDS_FROM_1970_TO_2000  = 946684800
    _DS3231M_REG_RTC_SEC        = 0X00
    _DS3231M_REG_RTC_MIN        = 0X01
    _DS3231M_REG_RTC_HOUR       = 0X02
    _DS3231M_REG_RTC_DAY        = 0X03
    _DS3231M_REG_RTC_DATE       = 0X04
    _DS3231M_REG_RTC_MONTH      = 0X05
    _DS3231M_REG_RTC_YEAR       = 0X06
    _DS3231M_REG_ALM1_SEC       = 0X07
    _DS3231M_REG_ALM1_MIN       = 0X08
    _DS3231M_REG_ALM1_HOUR      = 0X09
    _DS3231M_REG_ALM1_DAY       = 0X0A
    _DS3231M_REG_ALM2_MIN       = 0X0B
    _DS3231M_REG_ALM2_HOUR      = 0X0C
    _DS3231M_REG_ALM2_DAY       = 0X0D
    _DS3231M_REG_CONTROL        = 0x0E
    _DS3231M_REG_STATUS         = 0x0F
    _DS3231M_REG_AGE_OFFSET     = 0X10
    _DS3231M_REG_TEMPERATURE    = 0x11
    
    rtc_bcd[7] = 0
    bcd[7] = 0
    _ss = 0
    _mm = 0
    _hh = 0
    _d = 0
    _m = 0
    _y = 0
    daysOfTheWeek[7] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"}
    hourOfAM[4] = {"", "", "AM", "PM"} 


    def __init__():
        _deviceAddr = self._DS3231M_IIC_ADDRESS
        
  
    def date2days(self, y, m, d):
        if y >= 2000:
            y -= 2000
        days = d
        for (i = 1; i < m; ++i){
            days += pgm_read_byte(daysInMonth + i - 1)
        } if (m > 2 && y % 4 == 0)
            ++days
        return days + 365 * y + (y + 3) / 4 - 1

    def conv2d(self, p)
        v = 0
        if p >= '0' and p <= '9':
            v = p - '0'
        return 10 * v + ++p - '0'


    def bcd2bin(self, val):
        return val - 6 * (val >> 4)

    def bin2bcd (self, val):
        return val + 6 * (val / 10)

    def read_sqw_pin_mode(self):
        mode[1]
        read_reg(_DS3231M_REG_CONTROL, mode, 1)
        mode[0] &= 0x93
        return mode[0]

    def writeSqwPinMode(self, mode):
        ctrl[1] = 0
        read_reg(_DS3231M_REG_CONTROL, ctrl, 1)
        ctrl[0] &= ~0x04
        ctrl[0] &= ~0x18
        if mode == _DS3231M_OFF:
            ctrl[0] |= 0x04
        else:
            ctrl[0] |= mode
        write_reg(_DS3231M_REG_CONTROL, ctrl, 1);

    def dayOfTheWeek(self):
        day = self.date2days(_y, _m, _d)
        return (day + 6) % 7
    
    def getDayOfTheWeek(self):
        return self.daysOfTheWeek[self.dayOfTheWeek()]
    
    def setHour(self, hour, mode):
        self.hh = (mode << 5|self.bin2bcd(hour))
    
    def getAMorPM(self):
        buffer[1]
        read_reg(DS3231M_REG_RTC_HOUR, buffer, 1)
        buffer[0] = buffer[0] << 1
        buffer[0] = buffer[0] >> 6
        return hourOfAM[buffer[0]]
        
    def adjust(self):
        buffer[7] = {self.bin2bcd(ss),self.bin2bcd(mm),self.hh,self.dayOfTheWeek(),self.bin2bcd(d),self.bin2bcd(m),self.bin2bcd(y)}
        write_reg(_DS3231M_REG_RTC_SEC, buffer, 7)
        statreg[1]
        read_reg(_DS3231M_REG_STATUS, statreg, 1)
        statreg[0] &= ~0x80
        write_reg(_DS3231M_REG_STATUS, statreg, 1)
    
    def getNowTime(self):
        read_reg(_DS3231M_REG_RTC_SEC, self.bcd, 7)
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
    
    def getTemperatureC(self):
        buf[2]
        read_reg(_DS3231M_REG_TEMPERATURE, buf, 2)
        return ((float)buf[0] + (buf[1]>>6)*0.25f)
    
    def lostPower(self):
        status[1]
        read_reg(DS3231M_REG_STATUS, status, 1)
        return status[0] >> 7
    }
    
    def setAlarm(self, alarmType, date, hour, mode, minute, second, state ):
        dates[] = {self.bin2bcd(date)}
        hours[] = {mode << 5|self.bin2bcd(hour)}
        minutes[] = {self.bin2bcd(minute)}
        seconds[] = {self.bin2bcd(second)}
        days[] = {self.bin2bcd(dayOfTheWeek())}
        buffer[1]
        if alarmType >= UnknownAlarm:
            return
        if alarmType < EveryMinute:
            write_reg(_DS3231M_REG_ALM1_SEC, seconds, 1)
            write_reg(_DS3231M_REG_ALM1_MIN, minutes, 1)
            write_reg(_DS3231M_REG_ALM1_HOUR, hours, 1)
            if alarmType == SecondsMinutesHoursDateMatch:
                write_reg(_DS3231M_REG_ALM1_DAY, dates, 1)
            else:
                write_reg(_DS3231M_REG_ALM1_DAY, days, 1);
            if alarmType < SecondsMinutesHoursDateMatch:
                read_reg(_DS3231M_REG_ALM1_DAY, buffer, 1)
                buffer[0] |= 0x80
                write_reg(_DS3231M_REG_ALM1_DAY, buffer, 1)
            if alarmType < SecondsMinutesHoursMatch:
                read_reg(_DS3231M_REG_ALM1_HOUR, buffer, 1)
                buffer[0] |= 0x80
                write_reg(_DS3231M_REG_ALM1_HOUR, buffer, 1)
            if alarmType < SecondsMinutesMatch):
                read_reg(_DS3231M_REG_ALM1_MIN, buffer, 1)
                buffer[0] |= 0x80
                write_reg(_DS3231M_REG_ALM1_MIN, buffer, 1)
            if(alarmType == eEverySecond):
                read_reg(_DS3231M_REG_ALM1_SEC, buffer, 1)
                buffer[0] |= 0x80
                write_reg(_DS3231M_REG_ALM1_SEC, buffer, 1)
            if(alarmType == eSecondsMinutesHoursDayMatch):
                read_reg(_DS3231M_REG_ALM1_DAY, buffer, 1)
                buffer[0] |= 0x40
                write_reg(_DS3231M_REG_ALM1_DAY, buffer, 1)
            if state == True:
                read_reg(_DS3231M_REG_CONTROL, buffer, 1)
                buffer[0] |= 1
                write_reg(_DS3231M_REG_CONTROL, buffer, 1)
            else:
                read_reg(_DS3231M_REG_CONTROL, buffer, 1)
                buffer[0] &= 0xFE
                write_reg(_DS3231M_REG_CONTROL, buffer, 1)
        else:
            write_reg(_DS3231M_REG_ALM2_MIN, minutes, 1)
            write_reg(_DS3231M_REG_ALM2_HOUR, hours, 1)
            if alarmType == MinutesHoursDateMatch:
                write_reg(_DS3231M_REG_ALM2_DAY, dates, 1)
            elif alarmType == MinutesHoursDayMatch:
                days[0] |= 0x80
                write_reg(_DS3231M_REG_ALM2_DAY, days, 1)
            if alarmType < MinutesHoursDateMatch:
                read_reg(DS3231M_REG_ALM2_DAY, buffer, 1)
                buffer[0] |= 0x80;
                write_reg(DS3231M_REG_ALM2_DAY, buffer, 1)
            if alarmType < MinutesHoursMatch:
                read_reg(_DS3231M_REG_ALM2_HOUR, buffer, 1)
                buffer[0] |= 0x80
                write_reg(_DS3231M_REG_ALM2_HOUR, buffer, 1)
            if alarmType == EveryMinute:
                read_reg(_DS3231M_REG_ALM2_MIN, buffer, 1)
                buffer[0] |= 0x80
                write_reg(_DS3231M_REG_ALM2_MIN, buffer, 1)
            if state == True:
                read_reg(_DS3231M_REG_CONTROL, buffer, 1)
                buffer[0] |= 2
                write_reg(_DS3231M_REG_CONTROL, buffer, 1)
            else:
                read_reg(_DS3231M_REG_CONTROL, buffer, 1)
                buffer[0] &= 0xFD
                write_reg(_DS3231M_REG_CONTROL, buffer, 1)
        self.clearAlarm()
        return
    
    def enAbleAlarm1Int(self):
        crtl[1]
        read_reg(_DS3231M_REG_CONTROL, crtl, 1)
        crtl[0] |= 0x01
        write_reg(_DS3231M_REG_CONTROL, crtl, 1)
    
    def disAbleAlarm1Int(self):
        crtl[1]
        read_reg(_DS3231M_REG_CONTROL, crtl, 1)
        crtl[0] &= 0xFE
        write_reg(_DS3231M_REG_CONTROL, crtl, 1)
    
    def enAbleAlarm2Int(self:
        crtl[1]
        read_reg(_DS3231M_REG_CONTROL, crtl, 1)
        crtl[0] |= 0x02
        write_reg(_DS3231M_REG_CONTROL, crtl, 1)
    
    def disAbleAlarm2Int(self):
        crtl[1]
        read_reg(_DS3231M_REG_CONTROL, crtl, 1)
        crtl[0] &= 0xFD
        write_reg(_DS3231M_REG_CONTROL, crtl, 1)
    
    def isAlarm(self):
        status[1]
        read_reg(_DS3231M_REG_STATUS, status, 1)
        return status[0]&3
    
    def clearAlarm(self):
        status[1]
        read_reg(_DS3231M_REG_STATUS, status, 1)
        status[0] &= 0xFC
        write_reg(_DS3231M_REG_STATUS, status, 1)
    
    def enAble32k(self):
        status[1]
        read_reg(_DS3231M_REG_STATUS, status, 1)
        status[0] |= 0x08
        write_reg(_DS3231M_REG_STATUS, status, 1)
    
    def disAble32k(self):
        status[1]
        read_reg(_DS3231M_REG_STATUS, status, 1)
        status[0] &= 0xF7
        write_reg(_DS3231M_REG_STATUS, status, 1)


class DFRobot_Sensor_IIC(DFRobot_DS3231M):
    def __init__(self, bus, mode):
        self.i2cbus=smbus.SMBus(bus)
        self.i2c_addr = DFRobot_DS3231M._DS3231M_IIC_ADDRESS
        super().__init__(mode)

    def begin(self):
        return super().begin()

    def write_reg(self, reg, buff, size):
        self.i2cbus.write_i2c_block_data(self.i2c_addr, reg, buff)

    def read_reg(reg, buff, size)
        buff = self.i2cbus.read_i2c_block_data(self.i2c_addr, register) 
