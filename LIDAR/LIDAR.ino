/*
 Displaying velocity and acceleration from a garmin LIDAR Lite v3HP
 By: Samer Armaly
 Date: October 2nd, 2019
 License: This code is public domain under the condition that if we meet you must offer your firstborn child. I can then choose to either accept or reject it (FirstBornChild license).
 
 This LIDAR device is supposed to send serial data to a RPi in order to show the differences in velocity and acceleration between me and the car infront of me. 
 This connected with many other things is what makes up FlashCarPi.
 
 connect the LIDAR to the Arduino:
 Arduino 5V -> LIDAR 5V red
 GND -> GND black
 A5 -> SCL green
 A4 -> SDA blue
 A0 -> Enable orange
*/

#include <Wire.h> //Used for I2C
#include "Filter.h"
#include <avr/wdt.h> //We need watch dog for this program

#define    LIDARLite_ADDRESS   0x62          // Default I2C Address of LIDAR-Lite.
#define    RegisterMeasure     0x00          // Register to write to initiate ranging.
#define    MeasureValue        0x04          // Value to initiate ranging.
#define    RegisterHighLowB    0x8F          // Register to get both High and Low bytes in 1 call.

//GPIO declarations
//-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

byte statLED = 13; //On board status LED
byte en_LIDAR = A0; //Low makes LIDAR go to sleep, high is normal operation

//-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

unsigned long lastTime = 0;
long lastReading = 0;
int lastDistance = 0;
float newDistance;
float SmoothDistance;

const byte numberOfDeltaX = 8;
float DeltaX[numberOfDeltaX];
byte DeltaXspot = 0; //Keeps track of where we are within the DeltaX array

#define LOOPTIME 20

ExponentialFilter<float> FilteredDistance(15, newDistance);

void setup()
{
  wdt_reset(); //Pet the dog
  wdt_disable(); //We don't want the watchdog during init

  Serial.begin(115200);
  Wire.begin();
  pinMode(en_LIDAR, OUTPUT);
  pinMode(statLED, OUTPUT);
  enableLIDAR();
  while(readLIDAR() == 0)
  {
    Serial.println("Failed LIDAR read");
    delay(100);
  }

  delay(500);

  wdt_reset(); //Pet the dog
  wdt_enable(WDTO_250MS); //Unleash the beast
}

void loop()
{
  wdt_reset(); //Pet the dog

  //Each second blink the status LED
  if (millis() - lastTime > 1000)
  {
    lastTime = millis();

    if (digitalRead(statLED) == LOW)
      digitalWrite(statLED, HIGH);
    else
      digitalWrite(statLED, LOW);
  }

  //Take a reading every 20ms
  if (millis() - lastReading > (LOOPTIME-1)) // 49)
  {
    lastReading = millis();

    //velocity
    //-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    newDistance = readLIDAR();
    if(newDistance > 4000) newDistance = 0;
    
    FilteredDistance.Filter(newDistance);  // Go get distance in cm (exponential filter)
    SmoothDistance = FilteredDistance.Current();
    int deltaXDistance = lastDistance - SmoothDistance;
    lastDistance = SmoothDistance;

    //Scan delta array to see if this new delta is sane or not
    boolean safeDelta = true;
    for(int x = 0 ; x < numberOfDeltaX ; x++)
    {
      //We don't want to register jumps greater than 30cm in 50ms
      //But if we're less than 1000cm then maybe
      //30 works well
      if( abs(deltaXDistance - DeltaX[x]) > 30) safeDelta = false; 
    }  
    
    //Insert this new delta into the array
    if(safeDelta)
    {
      DeltaX[DeltaXspot++] = deltaXDistance;
      if (DeltaXspot >= numberOfDeltaX) DeltaXspot = 0; //Wrap this variable
    }

    //Get average of the current DeltaX array
    float avgDeltaX = 0.0;
    for (byte x = 0 ; x < numberOfDeltaX ; x++)
      avgDeltaX += (float)DeltaX[x];
    avgDeltaX /= numberOfDeltaX;
    
    float velocity = 22.36936 * (float)avgDeltaX / (float)LOOPTIME;
    //22.36936 comes from a big coversion from cm per ms to mile per hour
    //float mph = 22.36936 * velocity;
    //ceil(mph); //Round up to the next number. This is helpful if we're not displaying decimals.
    
    Serial.print(round(SmoothDistance * 0.01));
    Serial.print("|");
    Serial.print(round(velocity));
    Serial.println();
  }
}

//A watch dog friendly delay
void petFriendlyDelay(int timeMS)
{
  long current = millis();
  
  while(millis() - current < timeMS)
  {
    delay(1);
    wdt_reset(); //Pet the dog
  }
}

//Get a new reading from the distance sensor
int readLIDAR(void)
{
  int distance = 0;

  Wire.beginTransmission((int)LIDARLite_ADDRESS); // transmit to LIDAR-Lite
  Wire.write((int)RegisterMeasure); // sets register pointer to  (0x00)
  Wire.write((int)MeasureValue); // sets register pointer to  (0x04)
  Wire.endTransmission(); // stop transmitting

  delay(20); // Wait 20ms for transmit
  wdt_reset(); //Pet the dog

  Wire.beginTransmission((int)LIDARLite_ADDRESS); // transmit to LIDAR-Lite
  Wire.write((int)RegisterHighLowB); // sets register pointer to (0x8f)
  Wire.endTransmission(); // stop transmitting

  delay(20); // Wait 20ms for transmit
  wdt_reset(); //Pet the dog

  Wire.requestFrom((int)LIDARLite_ADDRESS, 2); // request 2 bytes from LIDAR-Lite

  if (Wire.available() >= 2) // if two bytes were received
  {
    distance = Wire.read(); // receive high byte (overwrites previous reading)
    distance = distance << 8; // shift high byte to be high 8 bits
    distance |= Wire.read(); // receive low byte as lower 8 bits
    return (distance);
  }
  else
  {
    Serial.println("Read fail");
    disableLIDAR();
    delay(100);
    enableLIDAR();

    return(0);
  }
}

//Sometimes the LIDAR stops responding. This causes it to reset
void disableLIDAR()
{
  digitalWrite(en_LIDAR, LOW);
}

void enableLIDAR()
{
  digitalWrite(en_LIDAR, HIGH);  
}

//Takes an average of readings on a given pin
//Returns the average
int averageAnalogRead(byte pinToRead)
{
  byte numberOfReadings = 8;
  unsigned int runningValue = 0;

  for (int x = 0 ; x < numberOfReadings ; x++)
    runningValue += analogRead(pinToRead);
  runningValue /= numberOfReadings;

  return (runningValue);
} 
