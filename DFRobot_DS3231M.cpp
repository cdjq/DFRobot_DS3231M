/*!
 * @file DFRobot_DS3231M.cpp
 * @brief 定义DFRobot_DS3231M 类的基础结构，基础方法的实现
 * @copyright	Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @licence     The MIT License (MIT)
 * @author [yufeng](yufeng.luo@dfrobot.com)
 * @version  V1.0
 * @d  2019-07-13
 * @https://github.com/DFRobot/DFRobot_DS3231M
 */

#include <DFRobot_DS3231M.h>
const uint8_t daysInMonth [] PROGMEM={31,28,31,30,31,30,31,31,30,31,30,31};

static uint16_t date2days(uint16_t y, uint8_t m, uint8_t d) {
    if (y >= 2000)
        y -= 2000;                              // Remove year offset
    uint16_t days = d;                          // Store numbers of days
    for (uint8_t i = 1; i < m; ++i){
    days += pgm_read_byte(daysInMonth + i - 1); // Add number of days for each month
    } if (m > 2 && y % 4 == 0)
        ++days;                                 // Deal with leap years
    return days + 365 * y + (y + 3) / 4 - 1;    // Return computed value
}

static long time2long(uint16_t days, uint8_t h, uint8_t m, uint8_t s){
    return ((days * 24L + h) * 60 + m) * 60 + s;
}

static uint8_t conv2d(const char* p) {
    uint8_t v = 0;
    if ('0' <= *p && *p <= '9')
        v = *p - '0';
    return 10 * v + *++p - '0';
}

DFRobot_DS3231M::~DFRobot_DS3231M() {}

bool DFRobot_DS3231M::begin(void)
{
    Wire.begin();
    delay(100);
    Wire.beginTransmission(_deviceAddr);
    if(Wire.endTransmission() == 0)
        return true;
    else
        return false;
}

uint8_t DFRobot_DS3231M::bcd2bin(uint8_t val){
    return val - 6 * (val >> 4);
}

uint8_t DFRobot_DS3231M::bin2bcd (uint8_t val){
    return val + 6 * (val / 10);
}

eDs3231MSqwPinMode_t DFRobot_DS3231M::readSqwPinMode(){
    int mode;
    mode = readReg8(DS3231M_REG_CONTROL);
    mode &= 0x93;
    return static_cast<eDs3231MSqwPinMode_t>(mode);
}

void DFRobot_DS3231M::writeSqwPinMode(eDs3231MSqwPinMode_t mode){
    uint8_t ctrl;
    ctrl = readReg8(DS3231M_REG_CONTROL);
    ctrl &= ~0x04;
    ctrl &= ~0x18;
    if (mode == eDS3231M_OFF) 
        ctrl |= 0x04;
    else
        ctrl |= mode;
    writeReg8(DS3231M_REG_CONTROL, ctrl);
}

void DFRobot_DS3231M::dateTime (const __FlashStringHelper* date, const __FlashStringHelper* time){
    char buff[11];
    memcpy_P(buff, date, 11);
    y = conv2d(buff + 9);
    // Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
    Serial.println(y);
    switch (buff[0]) {
        case 'J': m = (buff[1] == 'a') ? 1 : ((buff[2] == 'n') ? 6 : 7); break;
        case 'F': m = 2; break;
        case 'A': m = buff[2] == 'r' ? 4 : 8; break;
        case 'M': m = buff[2] == 'r' ? 3 : 5; break;
        case 'S': m = 9; break;
        case 'O': m = 10; break;
        case 'N': m = 11; break;
        case 'D': m = 12; break;
    }
    d = conv2d(buff + 4);
    memcpy_P(buff, time, 8);
    hh = conv2d(buff);
    mm = conv2d(buff + 3);
    ss = conv2d(buff + 6);
}

uint8_t DFRobot_DS3231M::dayOfTheWeek() const {
  uint16_t day = date2days(_y, _m, _d); // compute the number of days
  return (day + 6) % 7;                 // Jan 1, 2000 is a Saturday
} 

void DFRobot_DS3231M::adjust(){
    dateTime(F(__DATE__), F(__TIME__));
    writeReg8(DS3231M_REG_RTC_SEC,bin2bcd(ss));    // Write seconds, keep device off
    writeReg8(DS3231M_REG_RTC_MIN,bin2bcd(mm));    // Write the minutes value
    writeReg8(DS3231M_REG_RTC_HOUR,bin2bcd(hh));   // Also re-sets the 24Hour clock on
    writeReg8(DS3231M_REG_RTC_DAY,dayOfTheWeek()); // Update the weekday
    writeReg8(DS3231M_REG_RTC_DATE,bin2bcd(d));    // Write the day of month
    writeReg8(DS3231M_REG_RTC_MONTH,bin2bcd(m));   // Month, ignore century bit
    writeReg8(DS3231M_REG_RTC_YEAR,bin2bcd(y));    // Write the year
    uint8_t statreg = readReg8(DS3231M_REG_STATUS);
    statreg &= ~0x80; // flip OSF bit
    writeReg8(DS3231M_REG_STATUS, statreg);
}

void DFRobot_DS3231M::getNowTime(){
    readReg(DS3231M_REG_RTC_SEC, bcd, 7);
    _ss = bcd2bin(bcd[0] & 0x7F);
    _mm = bcd2bin(bcd[1]);
    _hh = bcd2bin(bcd[2]);
    _d = bcd2bin(bcd[4]);
    _m = bcd2bin(bcd[5]);
    _y = bcd2bin(bcd[6]) + 2000;
}

float DFRobot_DS3231M::getTemperature(){
    uint8_t buf[2];
    readReg(DS3231M_REG_TEMPERATURE, buf, 2);
    return ((float)buf[0] + (buf[1]>>6)*0.25f);
}

bool DFRobot_DS3231M::lostPower(void) {
    return (readReg8(DS3231M_REG_STATUS) >> 7);
}

void DFRobot_DS3231M::setAlarm(const uint8_t alarmType, int16_t days,int8_t hours,
                               int8_t minutes,int8_t seconds, const bool state ){
    if (alarmType >= eUnknownAlarm)
        return;
    if (alarmType < eEveryMinute){
        writeReg8(DS3231M_REG_ALM1_SEC,bin2bcd(seconds)); // Set seconds value
        writeReg8(DS3231M_REG_ALM1_MIN,bin2bcd(minutes)); // Set minutes value
        writeReg8(DS3231M_REG_ALM1_HOUR,bin2bcd(hours));  // Set hours value
        if (alarmType == eSecondsMinutesHoursDateMatch)
            writeReg8(DS3231M_REG_ALM1_DAY, bin2bcd(days));
        else
            writeReg8(DS3231M_REG_ALM1_DAY, bin2bcd(dayOfTheWeek()));
        if(alarmType<eSecondsMinutesHoursDateMatch)                                 
            writeReg8(DS3231M_REG_ALM1_DAY,readReg8(DS3231M_REG_ALM1_DAY)|0x80);
        if(alarmType<eSecondsMinutesHoursMatch)                                     
            writeReg8(DS3231M_REG_ALM1_HOUR,readReg8(DS3231M_REG_ALM1_HOUR)|0x80);
        if(alarmType<eSecondsMinutesMatch)                                          
            writeReg8(DS3231M_REG_ALM1_MIN,readReg8(DS3231M_REG_ALM1_MIN)|0x80);
        if(alarmType==eEverySecond)                                                 
            writeReg8(DS3231M_REG_ALM1_SEC,readReg8(DS3231M_REG_ALM1_SEC)|0x80);
        if(alarmType==eSecondsMinutesHoursDayMatch)                                 
            writeReg8(DS3231M_REG_ALM1_DAY,readReg8(DS3231M_REG_ALM1_DAY)|0x40);
        if (state) 
            writeReg8(DS3231M_REG_CONTROL,readReg8(DS3231M_REG_CONTROL)|1);         
        else 
            writeReg8(DS3231M_REG_CONTROL,readReg8(DS3231M_REG_CONTROL)&0xFE);      
    }
    else{
        writeReg8(DS3231M_REG_ALM2_MIN,bin2bcd(minutes));                           
        writeReg8(DS3231M_REG_ALM2_HOUR,bin2bcd(hours));                            
        if(alarmType == eMinutesHoursDateMatch)                                     
            writeReg8(DS3231M_REG_ALM2_DAY,bin2bcd(days));                          
        else
            if (alarmType == eMinutesHoursDayMatch)                                 
                writeReg8(DS3231M_REG_ALM2_DAY,bin2bcd(dayOfTheWeek() | 0x80));     
        if(alarmType < eMinutesHoursDateMatch) 
            writeReg8(DS3231M_REG_ALM2_DAY,readReg8(DS3231M_REG_ALM2_DAY) | 0x80);  
        if(alarmType < eMinutesHoursMatch)
            writeReg8(DS3231M_REG_ALM2_HOUR,readReg8(DS3231M_REG_ALM2_HOUR) | 0x80);
        if(alarmType == eEveryMinute)
            writeReg8(DS3231M_REG_ALM2_MIN, readReg8(DS3231M_REG_ALM2_MIN) | 0x80); 
        if (state) 
            writeReg8(DS3231M_REG_CONTROL, readReg8(DS3231M_REG_CONTROL)|2);
        else
            writeReg8(DS3231M_REG_CONTROL, readReg8(DS3231M_REG_CONTROL)&0xFD);
    } // of if-then-else use alarm 1 or 2
    clearAlarm(); // Clear the alarm state
    return;
}

bool DFRobot_DS3231M::isAlarm() {
    return (readReg8(DS3231M_REG_STATUS)&3); // Alarm if either of 2 LSBits set
}

void DFRobot_DS3231M::clearAlarm(){
    writeReg8(DS3231M_REG_STATUS, readReg8(DS3231M_REG_STATUS)&0xFC);
} 

uint8_t DFRobot_DS3231M::readReg8(uint8_t reg){
    uint8_t val[1];
    readReg(reg, val, 1);
    return val[0];
}

void DFRobot_DS3231M::writeReg8(uint8_t reg, uint8_t val){
    uint8_t buf[] = {val};
    writeReg(reg, buf, 1);
}

void DFRobot_DS3231M::writeReg(uint8_t reg, const void* pBuf, size_t size)
{
    if(pBuf == NULL){
        DBG("pBuf ERROR!! : null pointer");
    }
    uint8_t * _pBuf = (uint8_t *)pBuf;
    _pWire->beginTransmission(_deviceAddr);
    _pWire->write(&reg, 1);
    
    for(uint16_t i = 0; i < size; i++){
        _pWire->write(_pBuf[i]);
    }
    _pWire->endTransmission();
}

uint8_t DFRobot_DS3231M::readReg(uint8_t reg, const void* pBuf, size_t size)
{
    if(pBuf == NULL){
        DBG("pBuf ERROR!! : null pointer");
    }
    uint8_t * _pBuf = (uint8_t *)pBuf;
    _pWire->beginTransmission(_deviceAddr);
    _pWire->write(&reg, 1);
    
    if( _pWire->endTransmission() != 0){
        return 0;
    }

    _pWire->requestFrom(_deviceAddr, (uint8_t) size);
    for(uint16_t i = 0; i < size; i++){
        _pBuf[i] = _pWire->read();
    }
    return size;
}
