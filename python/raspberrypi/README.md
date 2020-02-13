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

To use this library, first download the library file, paste it into the RaspberryPi, then open the examples folder and run the demo in the folder.

## Methods

```Python

  '''
  @brief Init chip 
  @return True means IIC communication succeeds, False means it fails. 
  '''
  def begin(self)
  '''
  @brief Get current time data
  '''
  def get_now_time(self)
  
  '''
  @brief get year
  @return year
  '''
  def year(self)
  
  '''
  @brief get month
  @return month
  '''
  def  month(self)
  
  '''
  @brief get date
  @return date
  '''
  def  day(self)
  
  '''
  @brief get hour
  @return hour
  '''
  def hour(self)
  
  '''
  @brief get minute
  @return minute
  '''
  def minute(self)
  
  '''
  @brief get second
  @return second
  '''
  def  second(self)
  
  '''
  @brief get day of week
  @return day of week
  '''
  def get_day_of_the_week(self)
  
  '''
  @brief Set year
  @param Year 
  '''
  def set_year(self, year)
  
  '''
  @brief Set month
  @param Month
  '''
  def set_month(self, month)
  
  '''
  @brief Set Date 
  @param Date
  '''
  def set_date(self, date)
  
  '''
  @brief Set the hours and 12hours or 24hours
  @param hour:1-12 in 12hours,0-23 in 24hours
  @param mode:e24hours, eAM, ePM
  '''
  def set_hour(self, hour, mode)
  
  '''
  @brief Set minute 
  @param Minute
  '''
  def set_minute(self, minute)
  
  '''
  @brief Set second
  @param Second
  '''
  def set_second(self, second)
  
  '''
  @brief Adjust current time 
  '''
  def adjust()
  
  '''
  @brief output AM or PM of time 
  '''
  def get_AM_or_PM()
  
  '''
  @brief Get current temperature 
  @return Current temperautre, unit: ℃ 
  '''
  def get_temperature_C()
  
  '''
  @brief Judge if it is power-down 
  @return If retrun true, power down, time needs to reset false, work well. 
  '''
  def lost_power(def)
  
  '''
  @brief Read the value of pin sqw
  @return eDS3231M_OFF             = 0x01 # Off
  @n      eDS3231M_SquareWave_1Hz  = 0x00 # 1Hz square wave
  @n      eDS3231M_SquareWave_1kHz = 0x08 # 1kHz square wave
  @n      eDS3231M_SquareWave_4kHz = 0x10 # 4kHz square wave
  @n      eDS3231M_SquareWave_8kHz = 0x18 # 8kHz square wave
  '''
  def read_sqw_pin_mode(self)
  
  '''
  @brief Set the vaule of pin sqw
  @param mode eDS3231M_OFF             = 0x01 # Off
  @n          eDS3231M_SquareWave_1Hz  = 0x00 # 1Hz square wave
  @n          eDS3231M_SquareWave_1kHz = 0x08 # 1kHz square wave
  @n          eDS3231M_SquareWave_4kHz = 0x10 # 4kHz square wave
  @n          eDS3231M_SquareWave_8kHz = 0x18 # 8kHz square wave
  '''
  def write_sqw_pin_mode(self, mode)
  
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
  def set_alarm(self, alarmType, date, hour, mode, minute, second, state = True)
  
  '''
  @brief Judge if the alarm clock is triggered 
  @return true, triggered false, not trigger
  '''
  def is_alarm(self)
  '''
  @brief Clear trigger flag
  '''
  def clear_alarm(self)
  
  '''
  @brief enable or disable the interrupt of alarm 
  '''
  def enable_alarm1_int(self)
  def disable_alarm1_int(self)
  def enable_alarm2_int(self)
  def disable_alarm2_int(self)
  
  '''
  @brief enable the 32k output 
  '''
  def enable_32k(self)
  
  '''
  @brief disable the 32k output 
  '''
  def disable_32k(self)
```

## Compatibility

MCU                | Work Well    | Work Wrong   | Untested    | Remarks
------------------ | :----------: | :----------: | :---------: | -----
RaspberryPi        |      √       |              |             | 

## History

- Data 2020-2-14
- Version V1.0


## Credits

Written by(yufeng.luo@dfrobot.com), 2020. (Welcome to our [website](https:#www.dfrobot.com/))





