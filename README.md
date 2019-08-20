# DFRobot_DS3231M
这是一个高精度，高稳定性RTC时钟模块<br>
这个模块通过IIC通信，它的精度在±5%ppm(每天误差不超过0.432秒)，并且在全温度范围和全寿命期间都能保持这个精度<br>
这个模块兼容2.5-5.5V宽电压，电池供电时消耗电流低至2uA<br>
这个模块还有测试环境温度的功能，误差在±3℃以内<br>
这个模块没有采用传统晶振，而是采用MEMS(微机电系统)振荡器，具有极高的稳定性和极低的温度飘移<br>


![正反面svg效果图](https://github.com/ouki-wang/DFRobot_Sensor/raw/master/resources/images/SEN0245svg1.png)


## 产品链接（链接到英文商城）
    SKU：产品名称
   
## Table of Contents

* [Summary](#summary)
* [Installation](#installation)
* [Methods](#methods)
* [Compatibility](#compatibility)
* [History](#history)
* [Credits](#credits)

## Summary

这个库可以读取当前时间，通过最后一次编译的时间进行校准<br>
这个库可以用于设置闹钟在确定的时间触发<br>
这个库可以用于测量环境温度<br>

## Installation

To use this library, first download the library file, paste it into the \Arduino\libraries directory, then open the examples folder and run the demo in the folder.

## Methods

```C++

  DFRobot_DS3231M(TwoWire *pWire = &Wire){_pWire = pWire;};
  ~DFRobot_DS3231M();
  /*!
   *@brief 初始化芯片
   *@return True代表IIC通信成功，false代表通信失败
   */
  bool begin(void);
  /*!
   *@brief 获取当前时间数据
   */
  void getNowTime();
  
  /*!
   *@brief get year
   *@return year
   */
  uint16_t year();
  
  /*!
   *@brief get month
   *@return month
   */
  uint8_t  month();
  
  /*!
   *@brief get date
   *@return date
   */
  uint8_t  day();
  
  /*!
   *@brief get hour
   *@return hour
   */
  uint8_t  hour();
  
  /*!
   *@brief get minute
   *@return minute
   */
  uint8_t  minute();
  
  /*!
   *@brief get second
   *@return second
   */
  uint8_t  second();
  
  /*!
   *@brief get day of week
   *@return day of week
   */
  uint8_t  dayOfTheWeek() const ;
  
  /*!
   *@brief 校准当前时间
   */
  void adjust();
  
  /*!
   *@brief 获取当前温度
   *@return 当前温度，单位为摄氏度
   */
  float getTemperatureC();
  
  /*!
   *@brief 判断是否掉电
   *@return true为发生掉电，需要重设时间，false为未发生掉电
   */
  bool lostPower(void);
  
  /*!
   *@brief 读取sqw引脚的值
   *@return eDS3231M_OFF             = 0x01 // Off
   *@n      eDS3231M_SquareWave_1Hz  = 0x00 // 1Hz square wave
   *@n      eDS3231M_SquareWave_1kHz = 0x08 // 1kHz square wave
   *@n      eDS3231M_SquareWave_4kHz = 0x10 // 4kHz square wave
   *@n      eDS3231M_SquareWave_8kHz = 0x18 // 8kHz square wave
   */
  eDs3231MSqwPinMode_t readSqwPinMode();
  
  /*!
   *@brief 设置sqw引脚的值
   *@param mode eDS3231M_OFF             = 0x01 // Off
   *@n          eDS3231M_SquareWave_1Hz  = 0x00 // 1Hz square wave
   *@n          eDS3231M_SquareWave_1kHz = 0x08 // 1kHz square wave
   *@n          eDS3231M_SquareWave_4kHz = 0x10 // 4kHz square wave
   *@n          eDS3231M_SquareWave_8kHz = 0x18 // 8kHz square wave
   */
  void writeSqwPinMode(eDs3231MSqwPinMode_t mode);
  
  /*!
   *@brief 设置闹钟
   *@param alarmType 闹钟的工作模式typedef enum{
   *@n                                  eEverySecond,                         //每秒触发一次
   *@n                                  eSecondsMatch,                        //每分钟触发一次
   *@n                                  eSecondsMinutesMatch,                 //每小时触发一次
   *@n                                  eSecondsMinutesHoursMatch,            //每天触发一次
   *@n                                  eSecondsMinutesHoursDateMatch,        //每月触发一次
   *@n                                  eSecondsMinutesHoursDayMatch,         //每周触发一次//Alarm1
   *@n                                  eEveryMinute,                         //每分钟触发一次
   *@n                                  eMinutesMatch,                        //每小时触发一次
   *@n                                  eMinutesHoursMatch,                   //每天触发一次
   *@n                                  eMinutesHoursDateMatch,               //每月触发一次
   *@n                                  eMinutesHoursDayMatch,                //每周触发一次//Alarm2
   *@n                                  eUnknownAlarm
   *@n                                  }eAlarmTypes;
   *@param days    闹钟时间(天)
   *@param hours   闹钟时间(小时)
   *@param minutes 闹钟时间(分钟)
   *@param seconds 闹钟时间(秒)
   */
  void setAlarm(const uint8_t alarmType,int16_t days,int8_t hours,
                int8_t minutes,int8_t seconds, const bool state  = true);
  
  /*!
   *@brief 判断闹钟是否触发
   *@return true代表触发，false代表未触发
   */
  bool isAlarm();
  /*!
   *@brief 清除触发flag
   */
  void clearAlarm();
```

## Compatibility

MCU                | Work Well    | Work Wrong   | Untested    | Remarks
------------------ | :----------: | :----------: | :---------: | -----
Arduino uno        |      √       |              |             | 
Mega2560        |      √       |              |             | 
Leonardo        |      √       |              |             | 
ESP32        |      √       |              |             | 
micro:bit        |      √       |              |             | 


## History

- data 2019-8-19
- version V0.1


## Credits

Written by(yufeng.luo@dfrobot.com), 2019. (Welcome to our [website](https://www.dfrobot.com/))





