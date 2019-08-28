/*!
 * @file DFRobot_DS3231M.h
 * @brief 定义DFRobot_DS3231M 类的基础结构
 * @copyright	Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @licence     The MIT License (MIT)
 * @author [yufeng](yufeng.luo@dfrobot.com)
 * @version  V1.0
 * @date  2019-08-19
 * @url https://github.com/DFRobot/DFRobot_DS3231M
 */

#ifndef _DFRobot_DS3231M_H
#define _DFRobot_DS3231M_H

#if ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif
#include <Wire.h>


/*I2C ADDRESS*/
#define DS3231M_IIC_ADDRESS          0x68

#define SECONDS_FROM_1970_TO_2000    946684800
#define DS3231M_REG_RTC_SEC          0X00
#define DS3231M_REG_RTC_MIN          0X01
#define DS3231M_REG_RTC_HOUR         0X02
#define DS3231M_REG_RTC_DAY          0X03
#define DS3231M_REG_RTC_DATE         0X04
#define DS3231M_REG_RTC_MONTH        0X05
#define DS3231M_REG_RTC_YEAR         0X06
#define DS3231M_REG_ALM1_SEC         0X07
#define DS3231M_REG_ALM1_MIN         0X08
#define DS3231M_REG_ALM1_HOUR        0X09
#define DS3231M_REG_ALM1_DAY         0X0A
#define DS3231M_REG_ALM2_MIN         0X0B
#define DS3231M_REG_ALM2_HOUR        0X0C
#define DS3231M_REG_ALM2_DAY         0X0D
#define DS3231M_REG_CONTROL          0x0E  // Control register
#define DS3231M_REG_STATUS           0x0F  // Status register
#define DS3231M_REG_AGE_OFFSET       0X10
#define DS3231M_REG_TEMPERATURE      0x11  // temperature register
//打开这个宏，可以看到程序的详细运行过程
//#define ENABLE_DBG

#ifdef ENABLE_DBG
#define DBG(...) {Serial.print("[");Serial.print(__FUNCTION__); Serial.print("(): "); Serial.print(__LINE__); Serial.print(" ] "); Serial.println(__VA_ARGS__);}
#else
#define DBG(...)
#endif

typedef enum{
    eDS3231M_OFF             = 0x01, // 不输出方波，进入中断模式
    eDS3231M_SquareWave_1Hz  = 0x00, // 1Hz square wave
    eDS3231M_SquareWave_1kHz = 0x08, // 1kHz square wave
    eDS3231M_SquareWave_4kHz = 0x10, // 4kHz square wave
    eDS3231M_SquareWave_8kHz = 0x18  // 8kHz square wave
}eDs3231MSqwPinMode_t;

typedef enum{
    eEverySecond,                  //每秒重复一次
    eSecondsMatch,                 //每分钟重复一次
    eSecondsMinutesMatch,          //每小时重复一次
    eSecondsMinutesHoursMatch,     //每天重复一次
    eSecondsMinutesHoursDateMatch, //每月重复一次
    eSecondsMinutesHoursDayMatch,  //每周重复一次//Alarm1
    eEveryMinute,                  //每分钟重复一次
    eMinutesMatch,                 //每小时重复一次
    eMinutesHoursMatch,            //每天重复一次
    eMinutesHoursDateMatch,        //每月重复一次
    eMinutesHoursDayMatch,         //每周重复一次//Alarm2
    eUnknownAlarm
}eAlarmTypes;

class DFRobot_DS3231M
{
public:
    /**
     * @brief 构造函数
     * @param 传入Wire地址
     */
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
     *@brief 获取年
     *@return 年
     */
    uint16_t year()         const { return _y; }
    /*!
     *@brief 获取月
     *@return 月
     */
    uint8_t  month()        const { return _m; }
    /*!
     *@brief 获取日
     *@return 日
     */
    uint8_t  day()          const { return _d; }
    /*!
     *@brief 获取时
     *@return 时
     */
    uint8_t  hour()         const { return _hh; }
    /*!
     *@brief 获取分
     *@return 分
     */
    uint8_t  minute()       const { return _mm; }
    /*!
     *@brief 获取秒
     *@return 秒
     */
    uint8_t  second()       const { return _ss; }
    void setCentury(uint8_t c);
    /*!
     *@brief 设置年
     *@param 年
     */
    void setYear(uint8_t year)  { y = year + 30; }
    /*!
     *@brief 设置月
     *@param 月
     */
    void setMonth(uint8_t month)  { m = month; }
    /*!
     *@brief 设置日
     *@param 日
     */
    void setDate(uint8_t date)  { d = date; }
    /*!
     *@brief 设置时
     *@param 时
     */
    void setHour(uint8_t hour)  { hh = hour; }
    /*!
     *@brief 设置分
     *@param 分
     */
    void setMinute(uint8_t minute)  { mm = minute; }
    /*!
     *@brief 设置秒
     *@param 秒
     */
    void setSecond(uint8_t second)  { ss = second; }
    
    /*!
     *@brief get day of week
     *@return day of week
     */
    char* getDayOfTheWeek();
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
     *@return 读取值在枚举变量eDs3231MSqwPinMode_t中解释
     */
    eDs3231MSqwPinMode_t readSqwPinMode();
    
    /*!
     *@brief 设置sqw引脚的值
     *@param dt 传入值在枚举变量eDs3231MSqwPinMode_t中解释
     */
    void writeSqwPinMode(eDs3231MSqwPinMode_t mode);
    
    /*!
     *@brief 设置最后一次编译的时间为当前时间
     *@param date 传入编译时的日期
     *@param time 传入编译时的时间
     */
    void dateTime(const __FlashStringHelper* date, const __FlashStringHelper* time);
    
    /*!
     *@brief 设置闹钟
     *@param alarmType 闹钟的工作模式
     *@param days    闹钟时间(天)
     *@param hours   闹钟时间(小时)
     *@param minutes 闹钟时间(分钟)
     *@param seconds 闹钟时间(秒)
     */
    void setAlarm(const uint8_t alarmType,int16_t days,int8_t hours,int8_t minutes,int8_t seconds, const bool state  = true);
    /*!
     *@brief 判断闹钟是否触发
     *@return true代表触发，false代表未触发
     */
    bool isAlarm();
    /*!
     *@brief 清除触发
     */
    void clearAlarm();
    
    uint8_t rtc[7];
    

protected:
    virtual void writeReg(uint8_t reg, const void* pBuf, size_t size);
    virtual uint8_t readReg(uint8_t reg, const void* pBuf, size_t size);
    
    /*!
     *@brief BCD码转BIN码
     *@param val 传入BCD码
     *@return 返回BIN码
     */
    static uint8_t bcd2bin(uint8_t val);
    /*!
     *@brief BIN码转BCD码
     *@param val 传入BIN码
     *@return 返回BCD码
     */
    static uint8_t bin2bcd(uint8_t val);
    /*!
     *@brief 写入初始时间
     *@param date 写入初始日期
     *@param time 写入初始时间
     */
    
    uint8_t  dayOfTheWeek() const ;
    uint8_t y,   ///< Year Offset
            m,  ///< Months
            d,    ///< Days
            hh,   ///< Hours
            mm, ///< Minutes
            ss; ///< Seconds

private:
    TwoWire *_pWire;
    uint8_t _deviceAddr = DS3231M_IIC_ADDRESS;
    uint8_t rtc_bcd[7];
    uint8_t bcd[7];
    uint8_t  _ss,_mm,_hh,_d,_m;
    uint16_t _y;
    const char* daysOfTheWeek[7] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"}; 
};

#endif
