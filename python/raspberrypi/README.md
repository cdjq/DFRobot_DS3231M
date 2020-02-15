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

To use this library, first download into the RaspberryPi, then open the examples folder and run the demo in the folder.
* python get_time_and _tem.py

## Methods

```Python
  '''
  @brief Init chip 
  @return True means chip init succeeds, False means it fails. 
  '''
  begin()
  '''
  @brief Get current time data
  '''
  get_now_time()
  
  '''
  @brief get year of now
  @return year
  '''
  year()
  
  '''
  @brief get month of now
  @return month
  '''
  month()
  
  '''
  @brief get date of now
  @return date
  '''
  day()
  
  '''
  @brief get hour of now
  @return hour
  '''
  hour()
  
  '''
  @brief get minute of now
  @return minute
  '''
  minute()
  
  '''
  @brief get second of now
  @return second
  '''
  second()
  
  '''
  @brief get day of week
  @return day of week
  '''
  get_day_of_the_week()
  
  '''
  @brief Set year + 2000 (2020 is 20, 1970 is -30)
  @param Year 
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
  @brief Adjust current time 
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

RaspberryPi Version
Board                | Work Well    | Work Wrong   | Untested    | Remarks
------------------ | :----------: | :----------: | :---------: | -----
RaspberryPi2       |              |              |     √       | 
RaspberryPi3       |      √       |              |             | 
RaspberryPi4       |              |              |     √       | 

Python Version
Python                | Work Well    | Work Wrong   | Untested    | Remarks
------------------ | :----------: | :----------: | :---------: | -----
Python2            |      √       |              |             | 
Python3            |      √       |              |             | 

## History

- Data 2020-2-14
- Version V1.0


## Credits

Written by(yufeng.luo@dfrobot.com), 2020. (Welcome to our [website](https:#www.dfrobot.com/))





