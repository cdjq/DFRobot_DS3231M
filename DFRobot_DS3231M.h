/*!
 * @file DFRobot_DS3231M.h
 * @brief Define the basic structure of class DFRobot_DS3231M 
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
//Open this macro to see the detailed running process of the program 
//#define ENABLE_DBG

#ifdef ENABLE_DBG
#define DBG(...) {Serial.print("[");Serial.print(__FUNCTION__); Serial.print("(): "); Serial.print(__LINE__); Serial.print(" ] "); Serial.println(__VA_ARGS__);}
#else
#define DBG(...)
#endif
typedef enum{
    eDS3231M_OFF             = 0x01, // Not output square wave, enter interrupt mode 
    eDS3231M_SquareWave_1Hz  = 0x00, // 1Hz square wave
    eDS3231M_SquareWave_1kHz = 0x08, // 1kHz square wave
    eDS3231M_SquareWave_4kHz = 0x10, // 4kHz square wave
    eDS3231M_SquareWave_8kHz = 0x18  // 8kHz square wave
}eDs3231MSqwPinMode_t;


typedef enum{
    e24hours = 0,
    eAM = 2,
    ePM = 3
}ehours;

typedef enum{
    eEverySecond,                  //repeat in every second
    eSecondsMatch,                 //repeat in every minute
    eSecondsMinutesMatch,          //repeat in every hour
    eSecondsMinutesHoursMatch,     //repeat in every day
    eSecondsMinutesHoursDateMatch, //repeat in every month
    eSecondsMinutesHoursDayMatch,  //repeat in every week
    //Alarm1
    
    eEveryMinute,                  //repeat in every minute
    eMinutesMatch,                 //repeat in every hour
    eMinutesHoursMatch,            //repeat in every day
    eMinutesHoursDateMatch,        //repeat in every month
    eMinutesHoursDayMatch,         //repeat in every week
    //Alarm2
    
    eUnknownAlarm
}eAlarmTypes;

class DFRobot_DS3231M
{
    typedef struct {
        uint8_t   hour: 6;
        uint8_t   mode: 2;
    } __attribute__ ((packed)) sNow24Hour_t;
    
    typedef struct {
        uint8_t   hour: 5;
        uint8_t   mode: 3;
    } __attribute__ ((packed)) sNow12Hour_t;
    
    typedef struct {
        uint8_t   century: 1;
        uint8_t   month: 7;
    } __attribute__ ((packed)) sNowMonth_t;
    
    typedef struct {
        uint8_t   second: 7;
        uint8_t   able: 1;
    } __attribute__ ((packed)) sAlarmSecond_t;
    
    typedef struct {
        uint8_t   minute: 7;
        uint8_t   able: 1;
    } __attribute__ ((packed)) sAlarmMinute_t;
    
    typedef struct {
        uint8_t   hour: 6;
        uint8_t   mode: 1;
        uint8_t   able: 1;
    } __attribute__ ((packed)) sAlarm24Hour_t;
    
    typedef struct {
        uint8_t   hour: 5;
        uint8_t   mode: 2;
        uint8_t   able: 1;
    } __attribute__ ((packed)) sAlarm12Hour_t;
    
    typedef struct {
        uint8_t   hour;
        uint8_t   mode;
        uint8_t   able;
    } __attribute__ ((packed)) sAlarmxxHour_t;
    
    
    typedef struct {
        uint8_t   date: 6;
        uint8_t   dayOrDate: 1;
        uint8_t   able: 1;
    } __attribute__ ((packed)) sAlarmDate_t;
    
    /*
    register of control
        * ------------------------------------------------------------------------------------------
        * |    b7    |    b6    |    b5    |    b4    |    b3    |    b2    |    b1     |    b0    |
        * ------------------------------------------------------------------------------------------
        * |   ESOC   |   BBSQW  |   CONV   |          NA         |   INTCN  |   A2IE    |   A1IE   |
        * ------------------------------------------------------------------------------------------
    */
    typedef struct {
        uint8_t   A1IE: 1;
        uint8_t   A2IE: 1;
        uint8_t   Interrupt: 3;
        uint8_t   ConvTemperature: 1;
        uint8_t   SQW: 1;
        uint8_t   oscillator: 1;
    } __attribute__ ((packed)) sControl_t;
    
    /*
    register of status
        * ------------------------------------------------------------------------------------------
        * |    b7    |    b6    |    b5    |    b4    |    b3    |    b2    |    b1     |    b0    |
        * ------------------------------------------------------------------------------------------
        * |   OSF    |               NA               |  EN32KHZ |    BSY   |    A2F    |    A1F   |
        * ------------------------------------------------------------------------------------------
    */
    typedef struct {
        uint8_t   A1F: 1;
        uint8_t   A2F: 1;
        uint8_t   BSY: 1;
        uint8_t   en32kHZ: 4;
        uint8_t   OSF: 1;
    } __attribute__ ((packed)) sStatus_t;
    
public:
    
    /**
     * @brief Constructor 
     * @param Input Wire address
     */
    DFRobot_DS3231M(TwoWire *pWire = &Wire){_pWire = pWire;};
    ~DFRobot_DS3231M();
    /*!
     *@brief Init chip 
     *@return True means IIC communication succeeds, false means it fails.
     */
    bool begin(void);
    /*!
     *@brief Get current time data
     */
    void getNowTime();
    /*!
     *@brief Get year of now
     *@return Year
     */
    uint8_t getYear();
    /*!
     *@brief Get month of now
     *@return Month
     */
    uint8_t  getMonth();
    /*!
     *@brief Get day of now
     *@return Day
     */
    uint8_t  getDate();
    /*!
     *@brief Get hour of now
     *@return Hour
     */
    uint8_t  getHour();
    /*!
     *@brief Get minute of now
     *@return Minute
     */
    uint8_t  getMinute();
    /*!
     *@brief Get second of now
     *@return Second
     */
    uint8_t  getSecond();
    /*!
     *@brief Set year 
     *@param Year
     */
    void setYear(uint8_t year);
    /*!
     *@brief Set month 
     *@param Month
     */
    void setMonth(uint8_t month);
    /*!
     *@brief Set date
     *@param Date
     */
    void setDate(uint8_t date);
    /*!
     *@brief Set the hours and 12hours or 24hours
     *@param hour:1-12 in 12hours,0-23 in 24hours
     *@param mode:e24hours, eAM, ePM
     */
    void setHour(uint8_t hour, ehours mode);
    /*!
     *@brief Set minute
     *@param Minute 
     */
    void setMinute(uint8_t minute);
    /*!
     *@brief Set second
     *@param Second
     */
    void setSecond(uint8_t second);
    
    /*!
     *@brief get day of week
     *@return day of week
     */
    const char* getDayOfTheWeek();
    /*!
     *@brief Adjust current time 
     */
    void adjust();
    /*!
     *@brief Get current temperature 
     *@return Current temperautre, unit: ℃ 
     */
    float getTemperatureC();
    /*!
     *@brief Get current temperature 
     *@return Current temperautre, unit: ℉ 
     */
    float getTemperatureF();
    /*!
     *@brief Judge if it is power-down 
     *@return If retrun true, power down, time needs to reset; false, work well. 
     */
    bool isLostPower(void);
    /*!
     *@brief Read the value of pin sqw
     *@return Explanation of the readings in enumeration variable eDs3231MSqwPinMode_t
     */
    eDs3231MSqwPinMode_t readSqwPinMode();
    
    /*!
     *@brief Set the vaule of pin sqw
     *@param dt Explanation of the witten value in enumeration variable eDs3231MSqwPinMode_t
     */
    void writeSqwPinMode(eDs3231MSqwPinMode_t mode);
    
    /*!
     *@brief Set the last compiled time as the current time
     */
    void dateTime();
    
    /*!
     *@brief Set alarm clock 
     *@param alarmType Alarm working mode
     *@param days    Alarm clock (day)
     *@param hours   Alarm clock (hour)
     *@param minutes Alarm clock (minute)
     *@param seconds Alarm clock (second)
     */
    void setAlarm(eAlarmTypes alarmType,int16_t days,int8_t hours,ehours mode,int8_t minutes,int8_t seconds, const bool state  = true);
    
    /*!
     *@brief enable or disable the interrupt of alarm 
     */
    void enAbleAlarm1Int();
    void disAbleAlarm1Int();
    void enAbleAlarm2Int();
    void disAbleAlarm2Int();
    
    /*!
     *@brief output AM or PM of time 
     */
    const char* getAMorPM();
    
    /*!
     *@brief Judge if the alarm clock is triggered
     *@return true, triggered; false, not trigger
     */
    bool isAlarm();
    
    /*!
     *@brief Clear trigger 
     */
    void clearAlarm();
    
    /*!
     *@brief enable the 32k output 
     */
    void enAble32k();
    
    /*!
     *@brief disable the 32k output 
     */
    void disAble32k();
    
    
    uint8_t rtc[7];
    

protected:
    virtual void writeReg(uint8_t reg, const void* pBuf, size_t size);
    virtual uint8_t readReg(uint8_t reg, const void* pBuf, size_t size);
    
    /*!
     *@brief BCD code to BIN code
     *@param val Input BCD code
     *@return Return BIN code
     */
    static uint8_t bcd2bin(uint8_t val);
    /*!
     *@brief BIN code to BCD code
     *@param val Input BIN code
     *@return Return BCD code
     */
    static uint8_t bin2bcd(uint8_t val);
    /*!
     *@brief Write init time 
     *@param date Write init date 
     *@param time Write init time 
     */
    
    uint8_t  dayOfTheWeek() const ;

private:
    TwoWire *_pWire;
    uint8_t _deviceAddr = DS3231M_IIC_ADDRESS;
    uint8_t bcd[7];
    uint8_t year, month, date;
    uint8_t y,   ///< Year Offset
            m,  ///< Months
            d,    ///< Days
            hh,   ///< Hours
            mm, ///< Minutes
            ss; ///< Seconds
    sControl_t conReg;
    sStatus_t staReg;
    const char* daysOfTheWeek[7] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"}; 
    const char* hourOfAM[4] = {"", "", "AM", "PM"}; 
};

#endif
