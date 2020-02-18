# DFRobot_DS3231M

## Table of Contents

* [Summary](#summary)
* [Installation](#installation)
* [Methods](#methods)
* [Compatibility](#compatibility)
* [History](#history)
* [Credits](#credits)

## Summary

* Read the time the program was last compiled. <br>
* Set a alarm clock to trigger at a specified time. <br>
* Measure ambient temperature. <br>

## Installation

要使用这个库，首先下载这个库到树莓派，然后打开例程文件夹，要执行某个例程demox.py，<br>
在命令行中键入python demox.py执行，例如想要执行get_time_and_temp.py例程，您需要输入命令：
```Python
python get_time_and_temp.py
```
## Methods

```Python
  '''
  @brief Init chip 
  @return True means chip init succeeds, False means it fails. 
  '''
  begin()
  
  '''
  @brief 获取当前年份
  @return year
  '''
  get_year()
  
  '''
  @brief 获取当前月份
  @return month
  '''
  get_month()
  
  '''
  @brief 获取当前日期
  @return date
  '''
  get_date()
  
  '''
  @brief 获取当前小时数
  @return hour
  '''
  get_hour()
  
  '''
  @brief 获取当前分钟数
  @return minute
  '''
  get_minute()
  
  '''
  @brief 获取当前秒数
  @return second
  '''
  get_second()
  
  '''
  @brief get day of week
  @return day of week
  '''
  get_day_of_the_week()
  
  '''
  @brief Set year + 2000
  @param Year (20 means 2020, -30 means 1970)
  '''
  set_year(year)
  
  '''
  @brief Set month
  @param Month(1-12)
  '''
  set_month(month)
  
  '''
  @brief Set Date 
  @param Date(1-31)
  '''
  set_date(date)
  
  '''
  @brief Set the hours and 12hours or 24hours
  @param hour:1-12 in 12hours,0-23 in 24hours
  @param mode:H24hours, AM, PM
  '''
  set_hour(hour, mode)
  
  '''
  @brief Set minute
  @param Minute(0-59)
  '''
  set_minute(minute)
  
  '''
  @brief Set second
  @param Second(0-59)
  '''
  set_second(second)
  
  '''
  @brief 将设定好的时间写入rtc
  '''
  adjust()
  
  '''
  @brief output AM or PM of time 
  '''
  get_AM_or_PM()
  
  '''
  @brief Get current temperature 
  @return Current temperautre, unit: ℃ 
  '''
  get_temperature_C()
  
  '''
  @brief Get current temperature 
  @return Current temperautre, unit: ℉ 
  '''
  get_temperature_F()
  
  '''
  @brief Judge if it is power-down 
  @return If retrun true, power down, time needs to reset false, work well. 
  '''
  is_lost_power()
  
  '''
  @brief Read the value of pin sqw
  @return OFF             = 0x01 # Off
  @n      SquareWave_1Hz  = 0x00 # 1Hz square wave
  @n      SquareWave_1kHz = 0x08 # 1kHz square wave
  @n      SquareWave_4kHz = 0x10 # 4kHz square wave
  @n      SquareWave_8kHz = 0x18 # 8kHz square wave
  '''
  read_sqw_pin_mode()
  
  '''
  @brief Set the vaule of pin sqw
  @param mode OFF             = 0x01 # Off
  @n          SquareWave_1Hz  = 0x00 # 1Hz square wave
  @n          SquareWave_1kHz = 0x08 # 1kHz square wave
  @n          SquareWave_4kHz = 0x10 # 4kHz square wave
  @n          SquareWave_8kHz = 0x18 # 8kHz square wave
  '''
  write_sqw_pin_mode(mode)
  
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
  @param days    Alarm clock Day (day)
  @param hours   Alarm clock Hour (hour)
  @param mode:   H24hours, AM, PM
  @param minutes Alarm clock (minute)
  @param seconds Alarm clock (second)
  '''
  set_alarm(alarmType, date, hour, mode, minute, second)
  
  '''
  @brief Judge if the alarm clock is triggered 
  @return true, triggered false, not trigger
  '''
  is_alarm()
  '''
  @brief Clear trigger flag
  '''
  clear_alarm()
  
  '''
  @brief enable or disable the interrupt of alarm 
  '''
  enable_alarm1_int()
  disable_alarm1_int()
  enable_alarm2_int()
  disable_alarm2_int()
  
  '''
  @brief This module has a pin can output 32kHz wave, enable the 32k output 
  '''
  enable_32k()
  
  '''
  @brief This module has a pin can output 32kHz wave, disable the 32k output 
  '''
  disable_32k()
```

## Compatibility

* RaspberryPi Version

Board                | Work Well    | Work Wrong   | Untested    | Remarks
------------------ | :----------: | :----------: | :---------: | -----
RaspberryPi2       |              |              |     √       | 
RaspberryPi3       |      √       |              |             | 
RaspberryPi4       |              |              |     √       | 

* Python Version

Python                | Work Well    | Work Wrong   | Untested    | Remarks
------------------ | :----------: | :----------: | :---------: | -----
Python2            |      √       |              |             | 
Python3            |      √       |              |             | 

## History

- Data 2020-2-14
- Version V1.0


## Credits

Written by(yufeng.luo@dfrobot.com), 2020. (Welcome to our [website](https:#www.dfrobot.com/))





