/*!
 * @file setAlarms.ino
 * @brief ,设置闹钟
 * @n 实验现象：设置闹钟在12秒后触发
 *
 * @copyright	Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @licence     The MIT License (MIT)
 * @author [LuoYufeng](yufeng.luo@dfrobot.com)
 * @version  V0.1
 * @date  2019-07-19
 * @https://github.com/DFRobot/DFRobot_DS3231M
 */
#include "DFRobot_DS3231M.h"

DFRobot_DS3231M rtc;

char daysOfTheWeek[7][12] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};

void setup(void)
{
    Serial.begin(9600);
    delay(3000);
    /*在这里一致等到芯片初始化完成才能退出*/
    while(rtc.begin() != true){
        Serial.println("初始化芯片失败，请确认芯片连接是否正确");
        delay(1000);
    }
    rtc.getNowTime();
    rtc.writeSqwPinMode(eDS3231M_SquareWave_1Hz);
    Serial.println("Setting alarm with");
    rtc.setAlarm(eSecondsMinutesHoursDateMatch,19,15,46,12); // Alarm goes off in 12 seconds
    if (rtc.lostPower()) {
        Serial.println("RTC lost power, lets set the time!");
        // following line sets the RTC to the date & time this sketch was compiled
        rtc.adjust();
    }
}
void loop() {
    rtc.getNowTime();
    if (rtc.isAlarm()){ // If the alarm bit is set
        Serial.println("闹钟触发.");
        rtc.clearAlarm();
    }
    Serial.print(rtc.year(), DEC);
    Serial.print('/');
    Serial.print(rtc.month(), DEC);
    Serial.print('/');
    Serial.print(rtc.day(), DEC);
    Serial.print(" (");
    Serial.print(daysOfTheWeek[rtc.dayOfTheWeek()]);
    Serial.print(") ");
    Serial.print(rtc.hour(), DEC);
    Serial.print(':');
    Serial.print(rtc.minute(), DEC);
    Serial.print(':');
    Serial.print(rtc.second(), DEC);
    Serial.println();
    delay(1000);
}