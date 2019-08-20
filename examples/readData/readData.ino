/*!
 * @file readData.ino
 * @brief 显示当前时间
 * @n 实验现象：每3秒读取一次数据，并打印到串口
 *
 * @copyright	Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @licence     The MIT License (MIT)
 * @author [LuoYufeng](yufeng.luo@dfrobot.com)
 * @version  V0.1
 * @date  2019-08-19
 * @url https://github.com/DFRobot/DFRobot_CCS811
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
    /*!
     *@brief 设置sqw引脚的值
     *@param mode eDS3231M_OFF             = 0x01 // Off
     *@n          eDS3231M_SquareWave_1Hz  = 0x00 // 1Hz square wave
     *@n          eDS3231M_SquareWave_1kHz = 0x08 // 1kHz square wave
     *@n          eDS3231M_SquareWave_4kHz = 0x10 // 4kHz square wave
     *@n          eDS3231M_SquareWave_8kHz = 0x18 // 8kHz square wave
     */
    rtc.writeSqwPinMode(eDS3231M_SquareWave_1Hz);
    /*!
     *@brief 设置sqw引脚的值
     *@return mode eDS3231M_OFF             = 0x01 // Off
     *@n           eDS3231M_SquareWave_1Hz  = 0x00 // 1Hz square wave
     *@n           eDS3231M_SquareWave_1kHz = 0x08 // 1kHz square wave
     *@n           eDS3231M_SquareWave_4kHz = 0x10 // 4kHz square wave
     *@n           eDS3231M_SquareWave_8kHz = 0x18 // 8kHz square wave
     */
    //Serial.println(rtc.readSqwPinMode,HEX);
    /*!
     *@brief 判断是否掉电
     *@return true为发生掉电，需要重设时间，false为未发生掉电
     */
    if (rtc.lostPower()) {
        Serial.println("RTC lost power, lets set the time!");
        /*!
         *@brief 校准当前时间
         */
        rtc.adjust();
    }
}
void loop() {
    /*!
     *@brief 获取当前时间数据
     *@return 当前时间数据
     */
    rtc.getNowTime();
    Serial.print(rtc.year(), DEC);//year
    Serial.print('/');
    Serial.print(rtc.month(), DEC);//month
    Serial.print('/');
    Serial.print(rtc.day(), DEC);//date
    Serial.print(" (");
    Serial.print(daysOfTheWeek[rtc.dayOfTheWeek()]);//day of week
    Serial.print(") ");
    Serial.print(rtc.hour(), DEC);//hour
    Serial.print(':');
    Serial.print(rtc.minute(), DEC);//minute
    Serial.print(':');
    Serial.print(rtc.second(), DEC);//second
    Serial.println();
    Serial.print("Temperature: ");
    /*!
     *@brief 获取当前温度
     *@return 当前温度，单位为摄氏度
     */
    Serial.print(rtc.getTemperatureC());
    Serial.println(" C");
    delay(3000);
}