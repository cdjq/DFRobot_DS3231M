/*!
 * @file setAlarmInterrupt.ino
 * @brief Set alarm, and use interrput pin to trigger it
 * @n Experiment phenomenon: set the alarm clock to trigger at a specified time 
 * @n                        connect SQW pin with DIGITALPIN2
 * @n                        print information on serial port after the alarm clock is triggered.
 * @copyright	Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @licence     The MIT License (MIT)
 * @author [LuoYufeng](yufeng.luo@dfrobot.com)
 * @version  V0.1
 * @date  2019-08-19
 * @url https://github.com/DFRobot/DFRobot_DS3231M
 */
#include "DFRobot_DS3231M.h"

volatile  int8_t alarmFlag = 0;

DFRobot_DS3231M rtc;

void setup(void)
{
    Serial.begin(9600);
    delay(3000);
    /*Wait for the chip to be initialized completely, and then exit*/
    while(rtc.begin() != true){
        Serial.println("failed to init chip, please check if the chip connection is correct. ");
        delay(1000);
    }
    /*!
     *@brief Set the value of pin sqw
     *@param mode eDS3231M_OFF             = 0x01 // Not output square wave, enter interrupt mode
     *@n          eDS3231M_SquareWave_1Hz  = 0x00 // 1Hz square wave
     *@n          eDS3231M_SquareWave_1kHz = 0x08 // 1kHz square wave
     *@n          eDS3231M_SquareWave_4kHz = 0x10 // 4kHz square wave
     *@n          eDS3231M_SquareWave_8kHz = 0x18 // 8kHz square wave
     */
    rtc.writeSqwPinMode(eDS3231M_OFF);
    /*!
     *@brief Set alarm clock 
     *@param alarmType Alarm clock working mode typedef enum{
     *@n                                  eEverySecond,
     *@n                                  eSecondsMatch,
     *@n                                  eSecondsMinutesMatch,
     *@n                                  eSecondsMinutesHoursMatch,
     *@n                                  eSecondsMinutesHoursDateMatch,
     *@n                                  eSecondsMinutesHoursDayMatch, //Alarm1
     *@n                                  eEveryMinute,
     *@n                                  eMinutesMatch,
     *@n                                  eMinutesHoursMatch,
     *@n                                  eMinutesHoursDateMatch,
     *@n                                  eMinutesHoursDayMatch,        //Alarm2
     *@n                                  eUnknownAlarm
     *@n                                  }eAlarmTypes;
     *@param days    Alarm clock (day)
     *@param hours   Alarm clock (hour)
     *@param minutes Alarm clock (minute)
     *@param seconds Alarm clock (second)
     */
    rtc.setAlarm(eSecondsMinutesHoursDateMatch,/*date,0-30*/19,/*hour,0-23*/15,/*minute,0-59*/46,/*second,0-59*/12);
    /*!
     *@brief Judge if it is power-down 
     *@return if return true, power-down, time needs to reset; false, work well
     */
    if (rtc.lostPower()) {
        Serial.println("RTC lost power, lets set the time!");
        /*!
         *@brief Adjust the current time
         */
        rtc.setYear(19);//Set year, default in the 21st century. 
        rtc.setMonth(8);
        rtc.setDate(26);
        rtc.setHour(15);
        rtc.setMinute(12);
        rtc.setSecond(30);
        rtc.adjust();
    }
    attachInterrupt(0, interrupt, FALLING);
}
void loop() {
    /*!
     *@brief Judge if the alarm clock is triggered
     *@return true, triggered; false, not triggered
     */
    if(alarmFlag == 1){
        alarmFlag = 0;
        rtc.getNowTime();
        Serial.print(rtc.year(), DEC);
        Serial.print('/');
        Serial.print(rtc.month(), DEC);
        Serial.print('/');
        Serial.print(rtc.day(), DEC);
        Serial.print(" (");
        Serial.print(rtc.getDayOfTheWeek());
        Serial.print(") ");
        Serial.print(rtc.hour(), DEC);
        Serial.print(':');
        Serial.print(rtc.minute(), DEC);
        Serial.print(':');
        Serial.print(rtc.second(), DEC);
        Serial.println();
        delay(1000);
    }
    else
        delay(1000);
}

int ledF = 0;

void interrupt(){
  alarmFlag = 1;
  if(ledF) {
    digitalWrite(LED_BUILTIN, LOW);  
    ledF = 0;
  } else {
    digitalWrite(LED_BUILTIN, HIGH);   
    ledF = 1;
  }
}
