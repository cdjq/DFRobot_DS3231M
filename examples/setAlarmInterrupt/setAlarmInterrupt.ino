/*!
 * @file setAlarmInterrupt.ino
 * @brief ,设置闹钟,用中断引脚触发
 * @n 实验现象：设置闹钟在固定的时间触发
 * @n           将SQW脚与DIGITALPIN2连接
 * @n           闹钟触发后会在串口打印信息
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
    /*在这里一致等到芯片初始化完成才能退出*/
    while(rtc.begin() != true){
        Serial.println("初始化芯片失败，请确认芯片连接是否正确");
        delay(1000);
    }
    /*!
     *@brief 设置sqw引脚的值
     *@param mode eDS3231M_OFF             = 0x01 // 不输出方波，进入中断模式
     *@n          eDS3231M_SquareWave_1Hz  = 0x00 // 1Hz square wave
     *@n          eDS3231M_SquareWave_1kHz = 0x08 // 1kHz square wave
     *@n          eDS3231M_SquareWave_4kHz = 0x10 // 4kHz square wave
     *@n          eDS3231M_SquareWave_8kHz = 0x18 // 8kHz square wave
     */
    rtc.writeSqwPinMode(eDS3231M_OFF);
    /*!
     *@brief 设置闹钟
     *@param alarmType 闹钟的工作模式typedef enum{
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
     *@param days    闹钟时间(天)
     *@param hours   闹钟时间(小时)
     *@param minutes 闹钟时间(分钟)
     *@param seconds 闹钟时间(秒)
     */
    rtc.setAlarm(eSecondsMinutesHoursDateMatch,/*date,0-30*/19,/*hour,0-23*/15,/*minute,0-59*/46,/*second,0-59*/12);
    /*!
     *@brief 判断是否掉电
     *@return true为发生掉电，需要重设时间，false为未发生掉电
     */
    if (rtc.lostPower()) {
        Serial.println("RTC lost power, lets set the time!");
        /*!
         *@brief 校准当前时间
         */
        rtc.setYear(19);//设置年，默认21世纪
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
     *@brief 判断闹钟是否触发
     *@return true代表触发，false代表未触发
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