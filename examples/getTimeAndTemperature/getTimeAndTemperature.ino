/*!
 * @file getTimeAndTemperature.ino
 * @brief Show current time 
 * @n Experiment phenomenon: read data every 3 seconds and print it on serial port. 
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


void setup(void)
{
    Serial.begin(9600);
    delay(3000);
    /*Wait for the chip to be initialized completely, and then exit*/
    while(rtc.begin() != true){
        Serial.println("Failed to init chip, please check if the chip connection is fine. ");
        delay(1000);
    }
    /*!
     *@brief Set the vaule of pin sqw
     *@param mode eDS3231M_OFF             = 0x01 // Not output square wave, enter interrupt mode
     *@n          eDS3231M_SquareWave_1Hz  = 0x00 // 1Hz square wave
     *@n          eDS3231M_SquareWave_1kHz = 0x08 // 1kHz square wave
     *@n          eDS3231M_SquareWave_4kHz = 0x10 // 4kHz square wave
     *@n          eDS3231M_SquareWave_8kHz = 0x18 // 8kHz square wave
     */
    rtc.writeSqwPinMode(eDS3231M_SquareWave_1Hz);
    /*!
     *@brief Read the value of pin sqw
     *@return mode eDS3231M_OFF             = 0x01 // Off
     *@n           eDS3231M_SquareWave_1Hz  = 0x00 // 1Hz square wave
     *@n           eDS3231M_SquareWave_1kHz = 0x08 // 1kHz square wave
     *@n           eDS3231M_SquareWave_4kHz = 0x10 // 4kHz square wave
     *@n           eDS3231M_SquareWave_8kHz = 0x18 // 8kHz square wave
     */
    //Serial.println(rtc.readSqwPinMode,HEX);
    /*!
     *@brief Judge if it is power-down
     *@return If retrun true, power down, needs to reset time; false, work well.
     */
    if (rtc.lostPower()) {
        Serial.println("RTC lost power, lets set the time!");
        /*!
         *@brief Adjust current time
         */
        rtc.setYear(19);//Set year, default in the 21st century, input negative number for years in the 20th century.
        rtc.setMonth(8);
        rtc.setDate(26);
        rtc.setHour(15);
        rtc.setMinute(12);
        rtc.setSecond(30);
        rtc.adjust();
    }
}
void loop() {
    /*!
     *@brief Get current time data 
     *@return Current time data
     */
    rtc.getNowTime();
    Serial.print(rtc.year(), DEC);//year
    Serial.print('/');
    Serial.print(rtc.month(), DEC);//month
    Serial.print('/');
    Serial.print(rtc.day(), DEC);//date
    Serial.print(" (");
    Serial.print(rtc.getDayOfTheWeek());//day of week
    Serial.print(") ");
    Serial.print(rtc.hour(), DEC);//hour
    Serial.print(':');
    Serial.print(rtc.minute(), DEC);//minute
    Serial.print(':');
    Serial.print(rtc.second(), DEC);//second
    Serial.println();
    Serial.print("Temperature: ");
    /*!
     *@brief Get current temperature
     *@return Current temperautre, unit: ℃ 
     */
    Serial.print(rtc.getTemperatureC());
    Serial.println(" C");
    delay(3000);
}
