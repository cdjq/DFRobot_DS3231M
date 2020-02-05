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
    class sNow24Hour_t():
        _pack_ = 1
        _fields_=[('hour',c_ubyte,6),
                ('mode',c_ubyte,2)]
        def __init__(self, hour, mode):
            self.hour = hour
            self.mode = mode

    class sNow12Hour_t():
        _pack_ = 1
        _fields_=[('hour',c_ubyte,5),
                ('mode',c_ubyte,3)]
        def __init__(self, hour, mode):
            self.hour = hour
            self.mode = mode
    
    class sNowMonth_t():
        _pack_ = 1
        _fields_=[('century',c_ubyte,1),
                ('month',c_ubyte,7)]
        def __init__(self, century, month):
            self.century = century
            self.month = month
    
    class sAlarmSecond_t():
        _pack_ = 1
        _fields_=[('second',c_ubyte,7),
                ('able',c_ubyte,1)]
        def __init__(self, second, able):
            self.second = second
            self.able = able
    
    class sAlarmMinute_t():
        _pack_ = 1
        _fields_=[('minute',c_ubyte,7),
                ('able',c_ubyte,1)]
        def __init__(self, minute, able):
            self.minute = minute
            self.able = able
    
    class sAlarm24Hour_t():
        _pack_ = 1
        _fields_=[('hour',c_ubyte,6),
                ('mode',c_ubyte,1)
                ('able',c_ubyte,1)]
        def __init__(self, hour, mode, able):
            self.hour = hour
            self.mode = mode
            self.able = able
    
    class sAlarm12Hour_t():
        _pack_ = 1
        _fields_=[('hour',c_ubyte,5),
                ('mode',c_ubyte,2)
                ('able',c_ubyte,1)]
        def __init__(self, hour, mode, able):
            self.hour = hour
            self.mode = mode
            self.able = able
    
    class sAlarmxxHour_t():
        _pack_ = 1
        _fields_=[('hour'),
                ('mode')
                ('able')]
        def __init__(self, hour, mode, able):
            self.hour = hour
            self.mode = mode
            self.able = able
    
    
    class sAlarmDate_t():
        _pack_ = 1
        _fields_=[('date',c_ubyte,6),
                ('dayOrDate',c_ubyte,1)
                ('able',c_ubyte,1)]
        def __init__(self, date, dayOrDate, able):
            self.date = date
            self.dayOrDate = dayOrDate
            self.able = able

    class sControl_t():
        _pack_ = 1
        _fields_=[('A1IE',c_ubyte,1),
                ('A2IE',c_ubyte,1),
                ('INTCN',c_ubyte,3),
                ('CONV',c_ubyte,1),
                ('BBSQW',c_ubyte,1)],
                ('EOSC',c_ubyte,1)]
        def __init__(self, EOSC, BBSQW, CONV, INTCN, A2IE, A1IE):
            self.A1IE = A1IE
            self.A2IE = A2IE
            self.INTCN = INTCN
            self.CONV = CONV
            self.BBSQW = BBSQW
            self.EOSC = EOSC


    class sStatus_t():
        _pack_ = 1
        _fields_=[('A1F',c_ubyte,1),
                ('A2F',c_ubyte,1),
                ('BSY ',c_ubyte,1),
                ('EN32KHZ',c_ubyte,1),
                ('OSF',c_ubyte,4)]
        def __init__(self, A1F, A2F, BSY, EN32KHZ, OSF):
            self.A1F = A1F
            self.A2F = A2F
            self.BSY = BSY
            self.EN32KHZ = EN32KHZ
            self.OSF = OSF

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
        sControl_t mode
        read_reg(_DS3231M_REG_CONTROL, mode, 1)
        mode[0] &= 0x93
        return mode[0]

    def write_sqw_pin_mode(self, mode):
        ctrl[1] = 0
        read_reg(_DS3231M_REG_CONTROL, ctrl, 1)
        ctrl[0] &= ~0x04
        ctrl[0] &= ~0x18
        if mode == _DS3231M_OFF:
            ctrl[0] |= 0x04
        else:
            ctrl[0] |= mode
        write_reg(_DS3231M_REG_CONTROL, ctrl, 1);

    def day_of_the_week(self):
        day = self.date2days(_y, _m, _d)
        return (day + 6) % 7
    
    def getDayOfTheWeek(self):
        return self.daysOfTheWeek[self.dayOfTheWeek()]

	def setYear(self, year){
		data = self.bin2bcd(year + 30);
		write_reg(_DS3231M_REG_RTC_YEAR, data, 1);
	
	def setMonth(self, month){
		data = self.bin2bcd(month); 
		write_reg(_DS3231M_REG_RTC_MONTH, data, 1);
	
	def setDate(self, date){
		data = self.bin2bcd(date);
		write_reg(_DS3231M_REG_RTC_DATE, data, 1);

    def set_hour(self, hour, mode):
        if mode == 0:
            data = sNow24Hour_t()
			data.hour = bin2bcd(hour)
			data.mode = mode
            write_reg(_DS3231M_REG_RTC_HOUR, data, 1)
        else:
            data = sNow12Hour_t()
			data.hour = bin2bcd(hour)
			data.mode = mode
            write_reg(_DS3231M_REG_RTC_HOUR, data, 1)
    
    def get_AM_or_PM(self):
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
    
    def get_now_time(self):
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
    
    def get_temperature_C(self):
        buf[2]
        read_reg(_DS3231M_REG_TEMPERATURE, buf, 2)
        return ((float)buf[0] + (buf[1]>>6)*0.25f)
    
    def lost_power(self):
        status[1]
        read_reg(DS3231M_REG_STATUS, status, 1)
        return status[0] >> 7
    }
    
    def set_alarm(self, alarmType, date, hour, mode, minute, second, state ):
		conReg = sControl_t()
		read_reg(_DS3231M_REG_CONTROL, conReg, 1)
        dates = sAlarmDate_t()
		hours = sAlarmxxHour_t()
        if mode == 0:
            hours24 = sAlarm24Hour_t()
            hours.hour = hours24.hour
            hours.mode = hours24.mode
            hours.able = hours24.able
        else:
            hours12 = sAlarm12Hour_t()
            hours.hour = hours12.hour
            hours.mode = hours12.mode
            hours.able = hours12.able
        minutes = sAlarmMinute_t()
		seconds = sAlarmSecond_t()
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
                dates.able = 1
            if alarmType < SecondsMinutesHoursMatch:
                hours.able = 1
            if alarmType < SecondsMinutesMatch):
                minutes.able = 1
            if(alarmType == eEverySecond):
                seconds.able = 1
            if(alarmType == eSecondsMinutesHoursDayMatch):
                dates.dayOrDate = 1
            if state == True:
                conReg.A1IE = 0
            else:
                conReg.A1IE = 0
        else:
			if alarmType == MinutesHoursDateMatch:
				write_reg(DS3231M_REG_ALM2_DAY, &dates, 1);
			else if alarmType == eMinutesHoursDayMatch:
				days[0] |= 0x80;
				write_reg(DS3231M_REG_ALM2_DAY, &days, 1);
			}
			if alarmType < MinutesHoursDateMatch:
				dates.able = 1
			if alarmType < MinutesHoursMatch:
				hours.able = 1
			if alarmType == EveryMinute:
				minutes.able = 1
			if (state)
				conReg.A2IE = 1;
			else
				conReg.A2IE = 0;
			write_reg(DS3231M_REG_ALM2_MIN, &minutes, sizeof(minutes));
			write_reg(DS3231M_REG_ALM2_HOUR, &hours, sizeof(hours));
        self.clear_alarm()
        return
    
    def enable_alarm1_int(self):
        conReg = sControl_t()
		read_reg(_DS3231M_REG_CONTROL, conReg, 1)
        conReg.A1IE = 1
        write_reg(_DS3231M_REG_CONTROL, conReg, 1)
    
    def disable_alarm1_int(self):
        conReg = sControl_t()
		read_reg(_DS3231M_REG_CONTROL, conReg, 1)
        onReg.A1IE = 0
        write_reg(_DS3231M_REG_CONTROL, conReg, 1)
    
    def enable_alarm2_int(self:
        conReg = sControl_t()
        read_reg(_DS3231M_REG_CONTROL, conReg, 1)
        conReg.A2IE = 1
        write_reg(_DS3231M_REG_CONTROL, conReg, 1)
    
    def disable_alarm2_int(self):
        conReg = sControl_t()
        read_reg(_DS3231M_REG_CONTROL, conReg, 1)
        conReg.A2IE = 0
        write_reg(_DS3231M_REG_CONTROL, conReg, 1)
    
    def is_alarm(self):
        staReg = sStatus_t()
        read_reg(_DS3231M_REG_STATUS, staReg, 1)
        return staReg.A1F & staReg.A2F 
    
    def clear_alarm(self):
        staReg = sStatus_t()
		read_reg(_DS3231M_REG_STATUS, staReg, 1)
		staReg.A1F = 0;
        staReg.A2F = 0;
        write_reg(_DS3231M_REG_STATUS, staReg, 1)
    
    def enable_32k(self):
        staReg = sStatus_t()
		read_reg(_DS3231M_REG_STATUS, staReg, 1)
        staReg.en32kHZ = 1
        write_reg(_DS3231M_REG_STATUS, staReg, 1)
    
    def disable_32k(self):
        staReg = sStatus_t()
		read_reg(_DS3231M_REG_STATUS, staReg, 1)
        staReg.en32kHZ = 0
        write_reg(_DS3231M_REG_STATUS, staReg, 1)


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
